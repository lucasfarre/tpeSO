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
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC initcfunctions(void) {
    (void) Py_InitModule("cfunctions", Functions);
}


