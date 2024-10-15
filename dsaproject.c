#include <stdio.h>
//#include <conio.h>
#include <windows.h>
#include <mmsystem.h>

int main(){
    PlaySound(TEXT("C:\\projects\\soundthing\\UnderTheTree\\BirthdayKid.wav"),NULL,SND_ASYNC);
    system("PAUSE");
    return 0;
}