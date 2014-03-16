#include <stdio.h>      /*************  Read Lock Setter  *************/
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
int main()
{
  struct flock lock, savelock;
  int fd;
   
  fd = open("book.dat", O_RDONLY);
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
}