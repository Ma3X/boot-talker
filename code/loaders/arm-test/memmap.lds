SECTIONS {
/*
         . = 0x00000000;
         .text : { * (.text); }
*/
/*         .text 0x00800000 BLOCK(0x4000) : { * (.text); } */
		 .text 0x00800000 : { * (.text); }

/*
         . = 0x00000400;
         .data : { * (.data); }
*/
}
