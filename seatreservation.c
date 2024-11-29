#include <stdio.h>
#include <stdlib.h>

/*
*	C언어로 만든
	극장 좌석예약 프로그램
*/


int main(void) {
	int seat[7][9] = { 0 };	//좌석 표시
	int i, j;
	char reservation[3] = " ";
	char ch;
	int row=0, column=0;    //row : 열, column : 행

	for (;;) {

		printf("좌석을 예약하시겠습니까?(yes = y | no = n) :");
		scanf_s("%c", &ch, sizeof(char));
		//printf("좌석 예약: %c\n", ch);
		system("cls");
		if (ch == 'y' || ch == 'Y') {
			fflush(stdin);  	// enter까지 문자로 입력을 받으므로 fflush를 해준다.

			printf("┌────────────────────────────────────────────────┐\n");
			printf("│     ----------------screen----------------     │\n");
			printf("└────────────────────────────────────────────────┘\n\n\n");

			for (i = 0; i < 7; i++) {	//비어있는 좌석	
				printf("%c\t", 65 + i);
				for (j = 0; j < 9; j++) {
					if (seat[i][j] == 1) {
						printf("★ ");
						seat[column][row] = 1;
					}
					else {
						printf("□ ");
					}
				}
				putchar('\n');
			}
			printf("\n \t1  2  3  4  5  6  7  8  9  \n");		// 열


			printf("예약할 좌석을 선택해주세요.(알파벳대문자로 입력해주세요): ");	// A  B  C  D  E  F  G 행  
			scanf_s("%s", reservation, sizeof(reservation));			//65 66 67 68 69 70 71
											//(int)reservation[0] - 65  <-- 알파벳  (int)reservation[1]-48 <--일반숫자 
			if (reservation[0] > 71 || reservation[0]<65) {
				printf("잘못입력하셨습니다. 다시 입력해주세요.: ");	
				scanf_s("%s", reservation, sizeof(reservation));	//A  B  C  D  E  F  G 이 아닌 경우 다시 입력받는다.
			}
			
			ch = getchar();		
			column = reservation[0] - 65;
			row = reservation[1] - 48 - 1;	//-1을 해준다.  

			//printf("%d %d\n", column, row);

			seat[column][row] = 1;	// 1을 넣어 자리가 예매된 좌석 표시

			printf("┌───────────────────────────┐\n");
			printf("│   좌석이 예약되었습니다.  │\n");
			printf("└───────────────────────────┘\n\n\n");
		}else {
			printf("좌석 예약 취소\n");
			break;
		}

	}

	return 0;
}
