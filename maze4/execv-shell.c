#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <stdio.h>

extern int errno;

int main(int argc, char const *argv[])
{
	int ret = execv(argv[1],0);
	printf("%d\n", ret);
	int errnum = errno;
    printf("Value of errno: %d\n", errno);
    perror("Error printed by perror");
    printf("Error: %s\n", strerror( errnum ));
	return 0;
}