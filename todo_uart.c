#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_memmap.h"
#include "driverlib/debug.h"
#include "driverlib/gpio.h"
#include "driverlib/sysctl.h"
#include "driverlib/uart.h"  # esto es la libreria para el uart
#include "driverlib/timer.h"
#include "driverlib/interrupt.h"
#include "driverlib/pin_map.h"
#include "utils/uartstdio.c"
#include <string.h>
#ifdef DEBUG
void
__error__(char *pcFilename, uint32_t ui32Line)
{
    while(1);
}
#endif
uint32_t FS=120000000*1.5; //120 MHz
void timer0A_handler(void);
uint8_t switch_state=0;
char  msg[]="h";
char data[100]; // solo hemos usado esto
char c[100];
int aux=0;
#define TIMEOUT 1000000 
int
main(void)
{
    //puertos
    SysCtlClockFreqSet((SYSCTL_XTAL_25MHZ | SYSCTL_OSC_MAIN | SYSCTL_USE_PLL | SYSCTL_CFG_VCO_480), 120000000);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPION);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOJ);
    GPIOPinTypeGPIOOutput(GPIO_PORTN_BASE, 0x03); // PN0 y PN1
    GPIOPinTypeGPIOOutput(GPIO_PORTF_BASE, 0x13); // PF0 y PF4
    GPIOPinTypeGPIOInput(GPIO_PORTJ_BASE, 0x03); // PJ0 (USR_SW1) y PJ1 (USR_SW2)

    GPIOPadConfigSet(GPIO_PORTJ_BASE, 0x03, GPIO_STRENGTH_2MA, GPIO_PIN_TYPE_STD_WPU);

    GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x00); // Apaga PN0 y PN1
    GPIOPinWrite(GPIO_PORTF_BASE, 0x13, 0x00); // Apaga PF0 y PF4            
    // //TIMER
    // //enable the timer peripheral
    // SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER0);
    // // Set timer
    // TimerConfigure(TIMER0_BASE, TIMER_CFG_PERIODIC);
    // // Set the count time for Timer
    // TimerLoadSet(TIMER0_BASE, TIMER_A, FS);
    // //Enable processor interrupts
    // IntMasterEnable();
    // // Enable Interrupt
    // IntEnable(35);//INT_TIMER0A_TM4C129
    // // Enable timer A interrupt
    // TimerIntEnable(TIMER0_BASE, TIMER_TIMA_TIMEOUT);
    // // Enable the timer
    // TimerEnable(TIMER0_BASE, TIMER_A);
  //UART--------------------------------------------------------------------------------------------------------------------------
    //configurar puertos y periferico
    SysCtlPeripheralEnable(SYSCTL_PERIPH_UART0);
    SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOA);
    // de esta manera funciona con usb
    GPIOPinConfigure(GPIO_PA0_U0RX); //de recepcion
    GPIOPinConfigure(GPIO_PA1_U0TX); //de transimision
    GPIOPinTypeUART(GPIO_PORTA_BASE, 0x03);

    UARTStdioConfig(0, 9600, 120000000); // simepre se pone 0, 9600 son los baudios, frecuencia
    
    while(1)
    {   
        uint8_t buttonState = GPIOPinRead(GPIO_PORTJ_BASE, 0x01);
        // Changing the timer delay
        if (buttonState == 0x00 ) 
        {
            UARTprintf("motor1\n"); //para enviar datos por el uart y siempre se poner /n para que la otra placa detecte que es el final del mensaje... esto lpo recibe la rasp
            // tambien se envian nuemeros pero esto se convertira a texto 
        }
        uint8_t buttonState2 = GPIOPinRead(GPIO_PORTJ_BASE, 0x02);
        // Changing the timer delay
        if (buttonState2 == 0x00 ) 
        {
            UARTprintf("motor2\n");

        }
        while(UARTCharsAvail(UART0_BASE)){  // si esta habilitabo el uart
            UARTgets(data,100); // se almacenan los datos en esta cadena, si es que no se reciben acaracteres , esto se bloquea por eso se pone el while en el casa de que se haya recibido un mensaje
            if(strcmp(data, "buzzer") == 0){ // compara la cadena con el dato o señal enviada
                aux=1;
               // SysCtlDelay(80000000); // si se ponia aqui el delay habia un error, por eso auxiliar = 1
                break; 
            }
            else{
                aux=0;
                break;
            }
            
        }
        if(aux==1){
            GPIOPinWrite(GPIO_PORTF_BASE, 0x03, 0x03); 
            SysCtlDelay(80000000); // 120M/3 *cantidad de delay // entre envio y recepcion de datos hay pequeña espera sino, se bloquea  
            GPIOPinWrite(GPIO_PORTF_BASE, 0x03, 0x00);
               }
        
        SysCtlDelay(800000); // ~1 segundo (depende de clock)
    }
}
void timer0A_handler(void)
{
    // switch_state++;
    // // Clear timer
    // TimerIntClear(TIMER0_BASE, TIMER_TIMA_TIMEOUT);
    // if (switch_state == 1)  
    // {
    //     GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x00);
    //     GPIOPinWrite(GPIO_PORTF_BASE, 0x13, 0x00);
    // }
    // else if (switch_state == 2)  
    // {
    //     GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x00);
    //     GPIOPinWrite(GPIO_PORTF_BASE, 0x13, 0x01);
    // }
    // else if (switch_state == 3)  
    // {
    //     GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x00);
    //     GPIOPinWrite(GPIO_PORTF_BASE, 0x13, 0x11);
    // }
    // else if (switch_state == 4)  
    // {
    //     GPIOPinWrite(GPIO_PORTN_BASE, 0x03, 0x01);
    //     GPIOPinWrite(GPIO_PORTF_BASE, 0x13, 0x11);
    //     switch_state=0;
    // }
}
