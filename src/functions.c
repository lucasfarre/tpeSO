#include <Python.h>
#include <stdio.h>
#include <sys/types.h>   /***********  Write Lock Setter  *******/
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <sys/stat.h>

#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <arpa/inet.h>

static PyObject * py_printf(PyObject *self, PyObject *args) {
    const char *s;
    if (!PyArg_ParseTuple(args, "s", &s))
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

//(0, os.getpid(), 'Hola Mundo', ip, port)
static PyObject * py_sendpetition(PyObject *self, PyObject *args) {
		int id = 1, pid = 14, port = 8889;
		const char * data;
		const char * ip;
		if (!PyArg_ParseTuple(args, "iissi", &id, &pid, &data, &ip, &port))
	        return NULL;
		int socket_fd;
		//struct sockaddr_un name;
		/* Create the socket. */
		//socket_fd = socket(PF_LOCAL, SOCK_STREAM, 0);
		socket_fd = socket(PF_INET, SOCK_STREAM, 0);
		/* Store the server’s name in the socket address. */
		//name.sun_family = AF_LOCAL;
		struct sockaddr_in s;
		s.sin_family = AF_INET;
		//s.sin_addr.s_addr = inet_addr("10.0.1.22");
		s.sin_addr.s_addr = inet_addr(ip);
		s.sin_port = htons(port);
		//inet_pton(AF_INET, "10.0.1.22", &(s.sin_addr));
		//strcpy(s.sin_path, socket_name);
		/* Connect the socket. */
		connect(socket_fd, (struct sockaddr *)&s, sizeof(s));
		/* Write the text on the command line to the socket. */
		write_text(socket_fd, data);
		close(socket_fd);
		return Py_BuildValue("i", 0); // return 0;
}

int server(int client_socket) {
	while (1) {
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
		printf("%s\n", text);
		/* Free the buffer. */
		free(text);
		/* If the client sent the message “quit,” we’re all done. */
		if (!strcmp(text, "quit"))
			return 1;
	}
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
	socklen_t client_name_len;
	int client_socket_fd;
	int client_sent_quit_message;
	if (!PyArg_ParseTuple(args, "i", &socket_fd))
		return NULL;
	/* Accept a connection. */
	client_socket_fd = accept(socket_fd,(struct sockaddr *) &client_name, &client_name_len);
	if(client_socket_fd == -1 )
		printf("Error en el accept.\n");
	/* Handle the connection. */
	client_sent_quit_message = server(client_socket_fd);
	if(client_sent_quit_message == -1)
		printf("Error en el server.\n");
	/* Close our end of the connection. */
	if(close(client_socket_fd) < 0)
		printf("Error en el close.\n");
	return Py_BuildValue("i", client_sent_quit_message);
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
    struct flock lock, savelock;
    lock.l_start = 0;
    lock.l_len = 0;
    lock.l_pid = getpid();
    lock.l_type = F_WRLCK;   /* Test for any lock on any part of file. */
    lock.l_whence = SEEK_SET;
    savelock = lock;
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

static PyMethodDef Functions[] = {
    {"printf",  py_printf, METH_VARARGS, "printf"},
    {"lock1",  py_lock1, METH_VARARGS, "lock1"},
    {"lock2",  py_lock2, METH_VARARGS, "lock2"},
    {"lock",  py_lock, METH_VARARGS, "lock"},
    {"unlock",  py_unlock, METH_VARARGS, "unlock"},
    {"sendPetition",  py_sendpetition, METH_VARARGS, "sendPetition"},
    {"serverInit",  py_serverinit, METH_VARARGS, "serverInit"},
    {"serverConnect",  py_serverconnect, METH_VARARGS, "serverConnect"},
    {"serverDown",  py_serverdown, METH_VARARGS, "serverDown"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC initcfunctions(void) {
    (void) Py_InitModule("cfunctions", Functions);
}


