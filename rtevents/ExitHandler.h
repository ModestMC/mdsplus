#ifndef EXIT_HANDLER_H
#define EXIT_HANDLER_H
#include "Runnable.h"
#include "Lock.h"

class ExitHandler
{
	static Lock *lock;
	static void checkLock()
	{
		if(!lock) 
		{
			lock = new Lock();
			lock->initialize();
		}
	}
public:
	static int handlerIdx;
	static void atExit(Runnable *inHandl);
	static void dispose();
};

#endif
