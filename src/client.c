#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>
#include <arpa/inet.h>

/* Write TEXT to the socket given by file descriptor SOCKET_FD. */
void write_text(int socket_fd, const char* text) {
	/* Write the number of bytes in the string, including
	 NUL-termination. */
	int length = strlen(text) + 1;
	write(socket_fd, &length, sizeof(length));
	/* Write the string. */
	write(socket_fd, text, length);
}
int main(int argc, char* const argv[]) {
	const char* const socket_name = argv[1];
	const char* const message = argv[2];
	int socket_fd;
	//struct sockaddr_un name;
	/* Create the socket. */
	//socket_fd = socket(PF_LOCAL, SOCK_STREAM, 0);
	socket_fd = socket(PF_INET, SOCK_STREAM, 0);
	/* Store the server’s name in the socket address. */
	//name.sun_family = AF_LOCAL;
	struct sockaddr_in s;
	s.sin_family = AF_INET;
	s.sin_addr.s_addr = inet_addr("10.0.1.22");
	s.sin_port = htons(8888);
	//inet_pton(AF_INET, "10.0.1.22", &(s.sin_addr));
	//strcpy(s.sin_path, socket_name);
	/* Connect the socket. */
	connect(socket_fd, (struct sockaddr *)&s, sizeof(s));
	/* Write the text on the command line to the socket. */
	write_text(socket_fd, message);
	close(socket_fd);
	return 0;
}
