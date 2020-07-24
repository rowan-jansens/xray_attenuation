/*x-ray attenuation through the atmosphere
Coded by: Rowan Jansens
*/ 

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

int photons[125][6];

//Data table with values for calculating atmopsheric density
//https://en.wikipedia.org/wiki/Barometric_formula
//layer height(m), layer density(kg/m3), layer temp(k), layer lapse-rate(k/m)
double atmosphere[8][4] = {
  {0.000, 1.225000, 288.15, -0.0065},
  {11000, 0.363910, 216.65, 0.00000},
  {20000, 0.088030, 216.65, 0.00100},
  {32000, 0.013220, 228.65, 0.00280},
  {47000, 0.001430, 270.65, 0.00000},
  {51000, 0.000860, 270.65, -0.0028},
  {71000, 0.000064, 214.65, -0.0020},
  {100000, 0, 1, -1}  //0 density layer makes computation faster
};

int get_layer(double height){
  //determine atmosphere layer (0-7) to sorce atmospheric data
  int layer = 0;
  while (height >= atmosphere[layer+1][0] && layer < 7){
    layer++;
  }
  return layer;
}
  
double density(double height){
  int layer = get_layer(height);
 
  //source values from "atmosphere" datatable depending on layer
  double density, l_height, l_den, l_temp, l_lapse, base, exponent;
  l_height = atmosphere[layer][0];
  l_den = atmosphere[layer][1];
  l_temp = atmosphere[layer][2];
  l_lapse = atmosphere[layer][3];

  if (layer == 7){
    return 0;
  }
  else if (l_lapse != 0){
    //build the first equation and return result
    base = l_temp / (l_temp + l_lapse * (height - l_height));
    exponent = 1 + ((9.80665 * 0.0289644) / (8.3144598 * l_lapse));
    density = l_den * pow(base, exponent);
    return density;
  }
  else {
    //build the second equation and return result
    exponent = (-9.80665 * 0.0289644 * (height - l_height)) /
               (8.3144598 * l_temp);
    density = l_den * exp(exponent);
    return density;
  }
}

//integrate the density function (^above^) using trapezoidal riemann sums
//and divide to come up with average density for a particlar interval
//If the altitude is over 100 km, then return 0.
double average_density(double height, double interval){
  double i;
  double area = 0;
  double step = 0.25; //decreasing this number will increase run time and accuracy
  clock_t begin = clock();
  if(height <= 100000){
    for (i=height; i<(height+interval); i+=step){
      area += ((density(i) + density(i + step)) / 2) * step;
    }
    clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("Integrated in: %f\n", time_spent);
    return area / interval;
  }
  else{
    return 0;
  }
}

//make a matrix of different photon energies (1-125 keV)
//give each energy some photons acording to an arbitrary exponential decay function
int make_photons(double start_height){
  int i;
  for (i=0; i<125; i++){
    int energy = (i+1);
    photons[i][0] = energy;
    photons[i][1] = start_height;  //i.e. the altitude of detonation
    photons[i][2] = 1000 * pow(1-0.01, energy);  //decay function
  }
}

//calculate attenuation coeffiect for a group of photons of a certain energy
//equation comes from a gnuplot fit of NIST attenuation data
//https://physics.nist.gov/PhysRefData/XrayMassCoef/ComTab/air.html
double get_attcoe(double energy){
  double attcoe = 393.265 / (pow(energy, 2.89148) + 0.0990357) + 0.0449311;
  return attcoe;
}

double percent(double height, double interval, int energy){
  double percent = exp(-1 * get_attcoe(energy) * average_density(height, interval) * interval);
  return percent;
}

double surface_evolution(double start_height, double interval){

  int h, i, j;
  FILE * f = fopen("surface_evolution.dat", "w");
  make_photons(start_height);
  
  for(h=start_height; h<=100000; h+=interval){   //increment the altitude
    for (i=0; i<125; i+=5){   //loop through some of the energies
      //increasing the incriment will increase run time
      fprintf(f, "%d %d %d\n", photons[i][1], photons[i][0], photons[i][2]);  //save matrix to file
  }
    fprintf(f, "\n");
    for (i=0; i<125; i++){
      photons[i][1] = h + interval;  //update the "iteration-number" column in the matrix
      photons[i][2] *= percent(h, interval, photons[i][0]);  //update the "photon-number" column in the matrix
    }
  }
  fclose(f);
}

double before_after(double start_height, double end_height){
  int i;
  FILE * f = fopen("before_after.dat", "w");

  make_photons(start_height);
  for (i=0; i<125; i++){
    photons[i][3] = photons[i][2] * percent(start_height, end_height - start_height, photons[i][0]);
  }

  for (i=0; i<125; i++){
    fprintf(f, "%d,%d,%d\n", photons[i][0], photons[i][2], photons[i][3]);
  }
  fclose(f);
}


int main(){
  int j;
  int i = 0;
  
  double start_height = 40000; //altitude of detonation
  double end_height = 100000;
  double interval = 2000;
  //changing the interval should have no major effect on the final results
  //becuase the calculations are always made using a continuous density function
  //which is averaged out over the interval

  //printf("Enter Detonation Altitude (meters above MSL [0m-100000m]): ");
  // scanf("%lf", &start_height);
  

  surface_evolution(start_height, interval);
  //before_after(start_height, end_height);
  //printf("%f", get_attcoe(125));


  return 0;
}
