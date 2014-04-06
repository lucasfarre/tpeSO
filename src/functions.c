#include <Python.h>
#include <stdio.h>
#include <sys/types.h>   /***********  Write Lock Setter  *******/
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <sys/stat.h>

static PyObject * py_printf(PyObject *self, PyObject *args) {
    const char *s;
    if (!PyArg_ParseTuple(args, "s", &s))
        return NULL;
    printf("%s", s);
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
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC initcfunctions(void) {
    (void) Py_InitModule("cfunctions", Functions);
}
