#include <zephyr/kernel.h>
#include <math.h>
#include "confusion.h"
#include "adc.h"

/* 
  K-means algorithm should provide 6 center points with
  3 values x,y,z. Let's test measurement system with known
  center points. I.e. x,y,z are supposed to have only values
  1 = down and 2 = up
  
  CP matrix is thus the 6 center points got from K-means algoritm
  teaching process. This should actually come from include file like
  #include "KmeansCenterPoints.h"
  
  And measurements matrix is just fake matrix for testing purpose
  actual measurements are taken from ADC when accelerator is connected.
*/ 

// int CP[6][3]={
// 	                     {1,0,0},
// 						 {2,0,0},
// 						 {0,1,0},
// 						 {0,2,0},
// 						 {0,0,1},
// 						 {0,0,2}
// };

int measurements[6][3]={
                   {1,0,0},
						 {2,0,0},
						 {0,1,0},
						 {0,2,0},
						 {0,0,1},
						 {0,0,2}
};

int CM[6][6]= {0};

extern struct Measurement realMeasurement;


void printConfusionMatrix(void)
{
	printk("Confusion matrix = \n");
	printk("   cp1 cp2 cp3 cp4 cp5 cp6\n");
	for(int i = 0;i<6;i++)
	{
		printk("cp%d %d   %d   %d   %d   %d   %d\n",i+1,CM[i][0],CM[i][1],CM[i][2],CM[i][3],CM[i][4],CM[i][5]);
	}
}
int CP[6][3] = {\
   {1533, 1539, 1235},\
    {1835, 1534, 1536},\
    {1535, 1831, 1536},\
    {1540, 1534, 1834},\
    {1230, 1537, 1535},\
    {1534, 1234, 1535}};

int abs(int x){
	return x < 0 ? x*-1 : x;
}

void makeHundredFakeClassifications(void)
{
   /*******************************************
   Jos ja toivottavasti kun teet toteutuksen paloissa eli varmistat ensin,
   että etäisyyden laskenta 6 keskipisteeseen toimii ja osaat valita 6 etäisyydestä
   voittajaksi sen lyhyimmän etäisyyden, niin silloin voit käyttää tätä aliohjelmaa
   varmistaaksesi, että etäisuuden laskenta ja luokittelu toimii varmasti tunnetulla
   itse keksimälläsi sensoridatalla ja itse keksimilläsi keskipisteillä.
   *******************************************/
  for(int i=0; i<6; i++){
   for (int j=0; j<100; j++){
      makeOneClassificationAndUpdateConfusionMatrix(i);
   }
  }
}

void makeOneClassificationAndUpdateConfusionMatrix(int direction)
{
   /**************************************
   Tee toteutus tälle ja voit tietysti muuttaa tämän aliohjelman sellaiseksi,
   että se tekee esim 100 kpl mittauksia tai sitten niin, että tätä funktiota
   kutsutaan 100 kertaa yhden mittauksen ja sen luokittelun tekemiseksi.
   **************************************/
  printk("Making classification and updating confusion matrix\n");
	struct Measurement m = readADCValue();
   int winner = calculateDistanceToAllCentrePointsAndSelectWinner(m.x, m.y, m.z);
   CM[winner][direction] += 1;
}
void printDir(int dir){
   printk("Direction %d: %d %d %d \n", dir, CP[dir][0], CP[dir][1], CP[dir][2]);
}

int calculateDistanceToAllCentrePointsAndSelectWinner(int x,int y,int z)
{
   /***************************************
   Tämän aliohjelma ottaa yhden kiihtyvyysanturin mittauksen x,y,z,
   laskee etäisyyden kaikkiin 6 K-means keskipisteisiin ja valitsee
   sen keskipisteen, jonka etäisyys mittaustulokseen on lyhyin.
   ***************************************/
	int min_dis = INT_MAX;
	int min_id = 0;
	for(int i=0;i<6;i++){
		int x_dis = abs((x - CP[i][0]));
		int y_dis = abs((y - CP[i][1]));
		int z_dis = abs((z - CP[i][2]));
		int tot_dis = x_dis + y_dis + z_dis;
		if(tot_dis < min_dis){
			min_dis = tot_dis;
			min_id = i;
		}
	}
	return min_id;
}

void resetConfusionMatrix(void)
{
	for(int i=0;i<6;i++)
	{ 
		for(int j = 0;j<6;j++)
		{
			CM[i][j]=0;
		}
	}
}

