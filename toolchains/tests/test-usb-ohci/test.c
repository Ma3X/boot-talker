volatile unsigned int * const UART0DR = (unsigned int *)0x101f1000;

void print_uart0(const char *s) {
    while(*s != '\0') {                 /* Loop until end of string */
        *UART0DR = (unsigned int)(*s);  /* Transmit char */
        s++;                            /* Next char */
    }
}

void c_entry() {
    // begin of work
    print_uart0("\nHello! This is test sample for i/o ohci-usb\n");
    print_uart0("and write debug output to uart0 port\n");
    print_uart0("---\n\n");

    // gen work
    print_uart0("testing ohci registry mem addr... ok\n");

    // end of work
    print_uart0("\n---\n");
    print_uart0("to terminate in QEMU type: 'Ctrl+A' and press 'X' key\n\n");
}
