#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>
#include <arpa/inet.h>

/* Read text from the socket and print it out. Continue until the
 socket closes. Return nonzero if the client sent a “quit”
 message, zero otherwise. */
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
int main(int argc, char* const argv[]) {
	const char* const socket_name = argv[1];
	int socket_fd;
	//struct sockaddr_un name;
	struct sockaddr_in name;
	int client_sent_quit_message;
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
	/* Repeatedly accept connections, spinning off one server() to deal
	 with each client. Continue until a client sends a “quit” message. */
	do {
		struct sockaddr_in client_name;
		socklen_t client_name_len;
		int client_socket_fd;
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
	} while (!client_sent_quit_message);
	/* Remove the socket file. */
	if(close(socket_fd) < 0)
		printf("Error en el close.\n");
	if(unlink(socket_name) < 0)
		printf("Conexión Finalizada.\n");
	return 0;
}
