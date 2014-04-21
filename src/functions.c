#include <Python.h>
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <limits.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <arpa/inet.h>
#include <signal.h>
#include <errno.h>

/* Cola de Mensajes */
#include <sys/msg.h>
#include <sys/ipc.h>


// include common.h
#include <sys/sem.h>
#include <sys/shm.h>

#define SIZE 10000

//


static key_t semkey =  0xBEEF4;
static key_t memkey =  0xBEEF5;

static PyObject * py_getmem(PyObject *self, PyObject *args) {
	char * mem;
	int memid;
	if ( (memid = shmget(memkey, SIZE, IPC_CREAT|0666)) == -1 ) {
		printf("Error en shmget");
		return Py_BuildValue("i", -1);
	}
	if ( !(mem = shmat(memid, NULL, 0)) ) {
		printf("Error en shmat");
		return Py_BuildValue("i", -1);
	}
	return Py_BuildValue("l", mem);
}


static PyObject * py_memread(PyObject *self, PyObject *args) {
	char * mem;
	if (!PyArg_ParseTuple(args, "l", &mem))
		return Py_BuildValue("i", -1);
	return Py_BuildValue("s", mem);
}


static PyObject * py_memwrite(PyObject *self, PyObject *args) {
	char * mem;
	const char * s;
	if (!PyArg_ParseTuple(args, "ls", &mem, &s))
		return Py_BuildValue("i", -1);
	return Py_BuildValue("i", strcpy(mem, s));
}


static PyObject * py_initmutex(PyObject *self, PyObject *args) {
	int semid;
	if ( (semid = semget(semkey, 1, 0)) >= 0 )
		return Py_BuildValue("i", -1);

	if ( (semid = semget(semkey, 1, IPC_CREAT|0666)) == -1 )
		printf("Error en semget");
		return Py_BuildValue("i", -1);
	semctl(semid, 0, SETVAL, 1);
	return Py_BuildValue("i", semid);
}

static PyObject * py_enter(PyObject *self, PyObject *args) {
	int semid;
	if (!PyArg_ParseTuple(args, "i", &semid))
		return Py_BuildValue("i", -1);
	struct sembuf sb;
	sb.sem_num = 0;
	sb.sem_op = -1;
	sb.sem_flg = SEM_UNDO;
	semop(semid, &sb, 1);
	return Py_BuildValue("i", 0);
}

static PyObject * py_leave(PyObject *self, PyObject *args) {
	int semid;
	if (!PyArg_ParseTuple(args, "i", &semid))
		return Py_BuildValue("i", -1);
	struct sembuf sb;
	sb.sem_num = 0;
	sb.sem_op = 1;
	sb.sem_flg = SEM_UNDO;
	semop(semid, &sb, 1);
	return Py_BuildValue("i", 0);
}

static PyObject * py_memset(PyObject *self, PyObject *args) {
	void * s;
	int c;
	size_t n;
	if (!PyArg_ParseTuple(args, "liI", &s, &c, &n))
		return Py_BuildValue("i", -1);
	return Py_BuildValue("i", memset(s, c, n));
}

static PyObject * py_strcmp(PyObject *self, PyObject *args) {
	const char * s1;
	const char * s2;
	if (!PyArg_ParseTuple(args, "ii", &s1, &s2))
		return Py_BuildValue("i", -1);
	return Py_BuildValue("i", strcmp(s1, s2));
}

static PyObject * py_malloc(PyObject *self, PyObject *args) {
	int size;
	if (!PyArg_ParseTuple(args, "i", &size))
		return Py_BuildValue("i", NULL);
	return Py_BuildValue("l", calloc(size, sizeof(char)));
}

static PyObject * py_strcpy(PyObject *self, PyObject *args) {
	char * d;
	const char * s;
	if (!PyArg_ParseTuple(args, "is", &d, &s))
		return Py_BuildValue("i", -1);
	return Py_BuildValue("i", strcpy(d, s));
}


static key_t keyin = 0xBEEF0;
static key_t keyout = 0xBEEF1;

/* When a SIGUSR1 signal arrives, set this variable. */
volatile sig_atomic_t usr_interrupt = 0;

void 
synch_signal (int sig) {
	usr_interrupt = 1;
}

void
fatal(char *s)
{
	perror(s);
	exit(1);
}

void
quit(int sig)
{
	printf("Servidor termina por señal %d\n", sig);
	exit(0);
}

/*
void 
myhandler() {  
	// warning: function declaration isn’t a prototype
	signal(SIGUSR1,myhandler); //reset signal 
	printf("Signal Recibida\n");
}
*/

static PyObject * py_sendsignal(PyObject *self, PyObject *args) {
	int pid;
	if (!PyArg_ParseTuple(args, "i", &pid))
		return Py_BuildValue("i", -1);
    //printf("Signal Enviada\n");
	kill(pid,SIGUSR1);
	return Py_BuildValue("i",1);
}

static PyObject * py_recievesignal(PyObject *self, PyObject *args) {
	usr_interrupt = 0;
  	struct sigaction usr_action;
  	sigset_t block_mask;
	/* Establish the signal handler. */
  	sigfillset (&block_mask);
  	usr_action.sa_handler = synch_signal;
  	usr_action.sa_mask = block_mask;
  	usr_action.sa_flags = 0;
  	sigaction(SIGUSR1, &usr_action, NULL);
  	while (!usr_interrupt)
    	;
    //printf("Signal Recibida\n");
	return Py_BuildValue("i",0);
}

/*
static PyObject * py_createfile(PyObject *self, PyObject *args) {
      int fd;
      const char * name;
	  if (!PyArg_ParseTuple(args, "s", &name))
	      return Py_BuildValue("i", -1);
	  fd = open(name, O_CREAT | O_EXCL | O_RDWR, 0777);
	  return Py_BuildValue("i", fd);
}

static PyObject * py_closefile(PyObject *self, PyObject *args) {
      int fd;
	  if (!PyArg_ParseTuple(args, "i", &fd))
	      return Py_BuildValue("i", -1);
	  fd = close(fd);
	  return Py_BuildValue("i", fd);
}
*/

static PyObject * py_msgserverinit(PyObject *self, PyObject *args) {
	int qin, qout;
	signal(SIGINT, quit);
	if ( (qin = msgget(keyin, 0666|IPC_CREAT)) == -1 )
		fatal("Error msgget qin\n\n");
	if ( (qout = msgget(keyout, 0666|IPC_CREAT)) == -1 )
		fatal("Error msgget qout\n\n");
	return Py_BuildValue("{s:i,s:i}","qin",qin,"qout",qout);
}

static PyObject * py_msgserverrcv(PyObject *self, PyObject *args) {
	int qin;
	ssize_t n;
	struct {
		long mtype;
		char mtext[200];
	} msg;
	if (!PyArg_ParseTuple(args, "i", &qin))
		return Py_BuildValue("i", -1);
	n = msgrcv(qin, &msg, sizeof msg.mtext, 0, IPC_NOWAIT);
	//printf("Recibi %s\n", msg.mtext);
	return Py_BuildValue("{s:i,s:s}","id",msg.mtype,"mtext",msg.mtext);
	//if ( (n = msgrcv(qin, &msg, sizeof msg.mtext, 0, 0)) > 0 )
	//	printf("Servidor: %.*s", n, msg.mtext);
	//	return Py_BuildValue("{s:i,s:s}","id",msg.mtype,"mtext",msg.mtext);
}	

static PyObject * py_msgclientsendandreceive(PyObject *self, PyObject *args) {
	const char * data;
	int qin, qout;
	long n = 0;
	if (!PyArg_ParseTuple(args, "sii", &data, &qin, &qout))
		return Py_BuildValue("i", -1);
	struct {
		long mtype;
		char mtext[200];
	} msg;
	msg.mtype = 4;
	strcpy(msg.mtext,data);
	//msg.mtext = data;
	printf("%ld\n",msg.mtype);
	msgsnd(qout, &msg, n, IPC_NOWAIT);
	printf("Envie\n %s\n",msg.mtext);
	n = msgrcv(qin, &msg, sizeof msg.mtext, msg.mtype, IPC_NOWAIT);
	return Py_BuildValue("s",msg.mtext);
}

static PyObject * py_printf(PyObject *self, PyObject *args) {
    const char *s;
    if (!PyArg_ParseTuple(args, "l", &s))
        return NULL;
    printf("%s", s);
    return Py_BuildValue("i", 0); // return 0;
}

/* Write TEXT to the socket given by file descriptor SOCKET_FD. */
void write_text(int socket_fd, const char* text) {
	/* Write the number of bytes in the string, including
	 NUL-termination. */
	int length = strlen(text) + 1;
	write(socket_fd, &length, sizeof(length));
	/* Write the string. */
	write(socket_fd, text, length);
}

/* Write TEXT to the socket given by file descriptor SOCKET_FD. */
char * read_text(int socket_fd) {
	int length;
	char * text;
	/* First, read the length of the text message from the socket. If
	 read returns zero, the client closed the connection. */
	if (read(socket_fd, &length, sizeof(length)) == 0)
		return 0;
	/* Allocate a buffer to hold the text. */
	text = (char*) malloc(length);
	/* Read the text itself, and print it. */
	read(socket_fd, text, length);
	/* Free the buffer. */
	return text;
}


//(0, os.getpid(), 'Hola Mundo', ip, port)
static PyObject * py_clientinit(PyObject *self, PyObject *args) {
		int port;
		const char * ip;
		if (!PyArg_ParseTuple(args, "si", &ip, &port))
	        return Py_BuildValue("i", -1);
		int socket_fd;
		/* Create the socket. */
		socket_fd = socket(PF_INET, SOCK_STREAM, 0);
		/* Store the server's name in the socket address. */
		struct sockaddr_in s;
		s.sin_family = AF_INET;
		s.sin_addr.s_addr = inet_addr(ip);
		s.sin_port = htons(port);
		/* Connect the socket. */
		connect(socket_fd, (struct sockaddr *)&s, sizeof(s));
		return Py_BuildValue("i", socket_fd); // return 0;
}

static PyObject * py_getpeername(PyObject *self, PyObject *args) {
		int socket_fd, ret;
		if (!PyArg_ParseTuple(args, "i", &socket_fd))
			return Py_BuildValue("i", -1);
		struct sockaddr_in addr;
		ret = getpeername(socket_fd, (struct sockaddr *)&addr, sizeof(addr));
		if(ret == -1 && errno == ENOTCONN)
			return Py_BuildValue("i", -1);
		return Py_BuildValue("i", 0);
}

static PyObject * py_clientdown(PyObject *self, PyObject *args) {
		int socket_fd;
		if (!PyArg_ParseTuple(args, "i", &socket_fd))
			return Py_BuildValue("i", -1);
		close(socket_fd);
		return Py_BuildValue("i", socket_fd); // return 0;
}

static PyObject * py_clientsend(PyObject *self, PyObject *args) {
		const char * data;
		int socket_fd;
		if (!PyArg_ParseTuple(args, "is", &socket_fd, &data))
			return Py_BuildValue("i", -1);
		/* Write the text on the command line to the socket. */
		write_text(socket_fd, data);
		return Py_BuildValue("i", 0); // return 0;
}

static PyObject * py_clientrecieve(PyObject *self, PyObject *args) {
		char * data;
		int socket_fd;
		if (!PyArg_ParseTuple(args, "i", &socket_fd))
			return Py_BuildValue("s", NULL);
		data = read_text(socket_fd);
		PyObject * ret = Py_BuildValue("s", data);
		free(data);
		return ret; // return 0;
}

char * server(int client_socket) {
	int length;
	char* text;
	/* First, read the length of the text message from the socket. If
	 read returns zero, the client closed the connection. */
	if (read(client_socket, &length, sizeof(length)) == 0)
		return 0;
	/* Allocate a buffer to hold the text. */
	text = (char*) malloc(length);
	/* Read the text itself, and print it. */
	read(client_socket, text, length);
	/* Free the buffer. */
	return text;
}

static PyObject * py_serverinit(PyObject *self, PyObject *args) {
	const char* socket_name;
	int socket_fd;
	//struct sockaddr_un name;
	struct sockaddr_in name;
	if (!PyArg_ParseTuple(args, "s", &socket_name))
			        return NULL;
	/* Create the socket. */
	//socket_fd = socket(PF_LOCAL, SOCK_STREAM, 0);
	socket_fd = socket(PF_INET, SOCK_STREAM, 0);
	if(socket_fd == -1) {
		printf("Error al crear el socket.\n");
	}
	/* Indicate that this is a server. */
	name.sin_family = AF_INET;
	name.sin_addr.s_addr = INADDR_ANY;
	name.sin_port = htons(8889);
	//strcpy(name.sun_path, socket_name);
	if(bind(socket_fd, (const struct sockaddr *) &name, sizeof(name)) < 0)
		printf("Error al bindear.\n");
	/* Listen for connections. */
	if(listen(socket_fd, 5) < 0)
		printf("Error en el listen.\n");
	return Py_BuildValue("{s:i, s:s}", "socket_fd", socket_fd, "socket_name", socket_name);
}

/* Repeatedly accept connections, spinning off one server() to deal
 with each client. Continue until a client sends a “quit” message. */
static PyObject * py_serverconnect(PyObject *self, PyObject *args) {
	int socket_fd;
	struct sockaddr_in client_name;
	socklen_t client_name_len = sizeof(client_name);
	int client_socket_fd;
	if (!PyArg_ParseTuple(args, "i", &socket_fd))
		return NULL;
	/* Accept a connection. */
	client_socket_fd = accept(socket_fd,(struct sockaddr *) &client_name, &client_name_len);
	if(client_socket_fd == -1 )
		printf("Error en el accept.\n");
	/* Handle the connection. */
	//text = server(client_socket_fd);
	//PyObject * ret = Py_BuildValue("{s:s, s:i}", "json", text, "client_socket_fd", client_socket_fd);
	//free(text);
	return Py_BuildValue("i", client_socket_fd);
}

static PyObject * py_serverdisconnect(PyObject *self, PyObject *args) {
	int client_socket_fd;
	if (!PyArg_ParseTuple(args, "i", &client_socket_fd))
			return NULL;
	/* Close our end of the connection. */
	if(close(client_socket_fd) < 0)
		printf("Error en el close.\n");
		return Py_BuildValue("i", 0);
}

static PyObject * py_serverdown(PyObject *self, PyObject *args) {
	const char* socket_name;
	int socket_fd;
	if (!PyArg_ParseTuple(args, "is", &socket_fd, &socket_name))
			return NULL;
	/* Remove the socket file. */
	if(close(socket_fd) < 0)
		printf("Error en el close.\n");
	if(unlink(socket_name) < 0)
		printf("Conexión Finalizada.\n");
	return Py_BuildValue("i", 0);
}

static PyObject * py_lock(PyObject *self, PyObject *args) {
    int fd;
    if (!PyArg_ParseTuple(args, "i", &fd))
        return NULL;
    struct flock lock;
    lock.l_start = 0;
    lock.l_len = 0;
    lock.l_pid = getpid();
    lock.l_type = F_WRLCK;   /* Test for any lock on any part of file. */
    lock.l_whence = SEEK_SET;
    fcntl(fd, F_SETLKW, &lock);
    return Py_BuildValue("i", 0); // return 0;
}

static PyObject * py_unlock(PyObject *self, PyObject *args) {
    int fd;
    if (!PyArg_ParseTuple(args, "i", &fd))
        return NULL;
    struct flock unlock;
    unlock.l_start   = 0;
    unlock.l_len     = 0;
    unlock.l_pid = getpid();
    unlock.l_type    = F_UNLCK;
    unlock.l_whence  = SEEK_SET;
    fcntl(fd, F_SETLK, &unlock);
    return Py_BuildValue("i", 0); // return 0;
}

static PyObject * py_lock1(PyObject *self, PyObject *args) {
	  int fd;
      struct flock lock, savelock;
      fd = open("db.json", O_RDWR);
      lock.l_type    = F_WRLCK;   /* Test for any lock on any part of file. */
      lock.l_start   = 0;
      lock.l_whence  = SEEK_SET;
      lock.l_len     = 0;
      savelock = lock;
      fcntl(fd, F_GETLK, &lock);  /* Overwrites lock structure with preventors. */
      if (lock.l_type == F_WRLCK)
      {
         printf("Process %d has a write lock already!\n", lock.l_pid);
         exit(1);
      }
      else if (lock.l_type == F_RDLCK)
      {
         printf("Process %d has a read lock already!\n", lock.l_pid);
         exit(1);
      }
      else
         fcntl(fd, F_SETLK, &savelock);
      pause();
      return Py_BuildValue("i", 0); // return 0;
}

static PyObject * py_lock2(PyObject *self, PyObject *args) {
	  struct flock lock, savelock;
	  int fd;

	  fd = open("db.json", O_RDONLY);
	  lock.l_type = F_RDLCK;
	  lock.l_start = 0;
	  lock.l_whence = SEEK_SET;
	  lock.l_len = 50;
	  savelock = lock;
	  fcntl(fd, F_GETLK, &lock);
	  if (lock.l_type == F_WRLCK)
	  {
	      printf("File is write-locked by process %d.\n", lock.l_pid);
	      exit(1);
	  }
	  fcntl(fd, F_SETLK, &savelock);
	  pause();
      return Py_BuildValue("i", 0); // return 0;
}

static PyObject * py_createfifo(PyObject *self, PyObject *args) {
	const char * name;
	if (!PyArg_ParseTuple(args, "s", &name))
		return Py_BuildValue("i", -1);
	if (access(name, 0) == -1 && mknod(name, S_IFIFO|0666, 0) == -1) {
		printf("Error mknod\n");
		return Py_BuildValue("i", -1);
	}
	return Py_BuildValue("i", 0);
}

static PyObject * py_mkfifo(PyObject *self, PyObject *args) {
	char * name;
	int mode;
	if (!PyArg_ParseTuple(args, "si", &name, &mode))
		return Py_BuildValue("i", -1);
	mkfifo(name, mode);
	return Py_BuildValue("i", 0);
}

//static PyObject * py_fiforead(PyObject *self, PyObject *args) {
//	int fd, n;
//	const char * name;
//	char buf[200] = "\0";
//	char s[INT_MAX] = "\0";
//	char aux[INT_MAX] = "\0";
//	if (!PyArg_ParseTuple(args, "s", &name))
//		return Py_BuildValue("i", -1);
//	fd = open(name, O_RDONLY);
//	while ( (n = read(fd, buf, sizeof buf)) > 0 ) {
//		printf("Hijo lee del pipe: %.*s", n, buf);
//		sprintf(aux, "%.*s", n, buf);
//		strcat(s, aux);
////		if ( memcmp(buf, "end", 3) == 0 )
////			break;
//	}
//	printf("Hijo termina\n");
//	return Py_BuildValue("s", s);
//}
//
//static PyObject * py_fifowrite(PyObject *self, PyObject *args) {
//	int fd, n;
//	char * name, s;
//	char buf[INT_MAX];
//	if (!PyArg_ParseTuple(args, "ss", &name, &s))
//		return Py_BuildValue("i", -1);
//
//	fd = open(name, O_WRONLY);
//	while ((n = read(0, buf, sizeof buf)) > 0) {
//		write(fd, buf, n);
//	}
//	printf("Padre termina\n");
//
//	return Py_BuildValue("i", 0);
//}

static PyObject * py_read(PyObject *self, PyObject *args) {
	int fd;
	char * s;
	if (!PyArg_ParseTuple(args, "i", &fd))
		return Py_BuildValue("i", -1);
	s = read_text(fd);
	return Py_BuildValue("s", s);
}

ssize_t readn(int fd, void *vptr, size_t n) {
	size_t nleft;
	ssize_t nread;
	char *ptr;
	for (ptr = vptr, nleft = n; nleft > 0; nleft -= nread, ptr += nread)
		if ((nread = read(fd, ptr, nleft)) < 0) {
			if (errno == EINTR)
				nread = 0;
			else
				return -1;
		} else if (nread == 0)
			break;
	return n - nleft; /* 0 <= result <= n */
}

static PyObject * py_readn(PyObject *self, PyObject *args) {
	int fd, r;
	void * vptr;
	size_t n;
	if (!PyArg_ParseTuple(args, "iI", &fd, &n))
		return Py_BuildValue("n", -1);
	if((vptr = malloc(n)) == NULL)
		return Py_BuildValue("n", -1);
	r = readn(fd, vptr, n);
	return Py_BuildValue("[n, s]", r, vptr);
}

ssize_t writen(int fd, const void *vptr, size_t n) {
	size_t nleft;
	ssize_t nwritten;
	const char *ptr;
	for (ptr = vptr, nleft = n; nleft > 0; nleft -= nwritten, ptr += nwritten)
		if ((nwritten = write(fd, ptr, nleft)) < 0) {
			if (errno == EINTR)
				nwritten = 0;
			else
				return -1;
		} else if (nwritten == 0)
			break;
	return n - nleft; /* 0 <= result <= n */
}

static PyObject * py_writen(PyObject *self, PyObject *args) {
	int fd;
	void * vptr;
	size_t n;
	if (!PyArg_ParseTuple(args, "isI", &fd, &vptr, &n))
		return Py_BuildValue("n", -1);
	return Py_BuildValue("n", writen(fd, vptr, n));
}

static PyObject * py_write(PyObject *self, PyObject *args) {
	int fd, length;
	char * s;
	if (!PyArg_ParseTuple(args, "isi", &fd, &s, &length))
		return Py_BuildValue("i", -1);	
	write(fd, s, length);
	return Py_BuildValue("i", 0);
}

void signal_handler(int signal) {
	printf("SIGPIPE HANDLER");
}

static PyObject * py_signal(PyObject *self, PyObject *args) {
	signal(SIGPIPE, signal_handler);
	return Py_BuildValue("i", 0);
}

static PyMethodDef Functions[] = {
    {"printf",  py_printf, METH_VARARGS, "printf"},
    {"lock1",  py_lock1, METH_VARARGS, "lock1"},
    {"lock2",  py_lock2, METH_VARARGS, "lock2"},
    {"lock",  py_lock, METH_VARARGS, "lock"},
    {"unlock",  py_unlock, METH_VARARGS, "unlock"},
    {"serverInit",  py_serverinit, METH_VARARGS, "serverInit"},
    {"serverConnect",  py_serverconnect, METH_VARARGS, "serverConnect"},
    {"serverDown",  py_serverdown, METH_VARARGS, "serverDown"},
    {"serverDisconnect",  py_serverdisconnect, METH_VARARGS, "serverDisconnect"},
    {"createFifo",  py_createfifo, METH_VARARGS, "createFifo"},
    {"clientDown",  py_clientdown, METH_VARARGS, "clientDown"},
    {"clientInit",  py_clientinit, METH_VARARGS, "clientInit"},
    {"clientSend",  py_clientsend, METH_VARARGS, "clientSend"},
    {"clientRecieve",  py_clientrecieve, METH_VARARGS, "clientRecieve"},
    {"getPeerName",  py_getpeername, METH_VARARGS, "getPeerName"},
    {"read",  py_read, METH_VARARGS, "read"},
    {"write",  py_write, METH_VARARGS, "write"},
//    {"fifoRead",  py_fiforead, METH_VARARGS, "fifoRead"},
//    {"fifoWrite",  py_fifowrite, METH_VARARGS, "fifoWrite"},
    {"mkfifo",  py_mkfifo, METH_VARARGS, "mkfifo"},
    {"signal",  py_signal, METH_VARARGS, "signal"},
    {"readn",  py_readn, METH_VARARGS, "readn"},
    {"writen",  py_writen, METH_VARARGS, "writen"},
    {"msgServerInit",  py_msgserverinit, METH_VARARGS, "msgServerInit"},
    {"msgServerRecieve",  py_msgserverrcv, METH_VARARGS, "msgServerRecieve"},
    {"msgClientSendAndReceive",  py_msgclientsendandreceive, METH_VARARGS, "msgClientSendAndReceive"},
//	{"createFile",  py_createfile, METH_VARARGS, "createFile"},
//	{"closeFile",  py_closefile, METH_VARARGS, "closeFile"},
	{"sendSignal",  py_sendsignal, METH_VARARGS, "sendSignal"},
	{"recieveSignal",  py_recievesignal, METH_VARARGS, "recieveSignal"},
	{"enter",  py_enter, METH_VARARGS, "enter"},
	{"leave",  py_leave, METH_VARARGS, "leave"},
	{"getmem",  py_getmem, METH_VARARGS, "getmem"},
	{"initmutex",  py_initmutex, METH_VARARGS, "initmutex"},
	{"memset",  py_memset, METH_VARARGS, "memset"},
	{"strcmp",  py_strcmp, METH_VARARGS, "strcmp"},
	{"malloc",  py_malloc, METH_VARARGS, "malloc"},
	{"strcpy",  py_strcpy, METH_VARARGS, "strcpy"},
	{"memread",  py_memread, METH_VARARGS, "memread"},
	{"memwrite",  py_memwrite, METH_VARARGS, "memwrite"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC initcfunctions(void) {
    (void) Py_InitModule("cfunctions", Functions);
//    PyObject *m;
//    PyModule_AddIntConstant(m, "SIZE", SIZE);
}

//
