#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double interval;
int photons[125][4];

//Data table with values for calculating atmopsheric density
//https://en.wikipedia.org/wiki/Barometric_formula
//layer height(m), layer density(kg/m3), layer temp(k), layer lapse-rate(k/m)
double atmosphere[7][4] = {
  {0.000, 1.225000, 288.15, -0.0065},
  {11000, 0.363910, 216.65, 0.00000},
  {20000, 0.088030, 216.65, 0.00100},
  {32000, 0.013220, 228.65, 0.00280},
  {47000, 0.001430, 270.65, 0.00000},
  {51000, 0.000860, 270.65, -0.0028},
  {71000, 0.000064, 214.65, -0.0020}
};

double density(double height){
  //determine what layer in the atmosphere (from the table) we are in
  int layer = 0;
  while (height > atmosphere[layer+1][0] && layer < 7){
    layer++;
  }

  //source values from "atmosphere" datatable depending on layer
  double density, l_height, l_den, l_temp, l_lapse, base, exponent;
  l_height = atmosphere[layer][0];
  l_den = atmosphere[layer][1];
  l_temp = atmosphere[layer][2];
  l_lapse = atmosphere[layer][3];

  if (l_lapse != 0){
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

//integrate the density function (above) and divide to come up with
//average density for a particlar interval
double average_density(double height){
  double i;
  double area = 0;
  double step = 0.5;
  for (i=height; i<(height+interval); i+=step){
    area += ((density(i) + density(i + step)) / 2) * step;
  }
  return area / interval;
}

//make a matrix of different photon energies (1-125 keV)
//give each energy 1 mil initial photons
int make_photons(double start_height){
  int i;
  for (i=0; i<125; i++){
    int energy = (i+1);
    photons[i][0] = energy;
    photons[i][1] = start_height;
    photons[i][2] = 1000 * pow(1-0.01, energy);
  }
}

//print the photon matrix to a file
int print_photons(){
  int i;
  for (i=0; i<125; i+=1){
    printf("%d %d %d\n", photons[i][0], photons[i][1], photons[i][2]);  
  }
}

//calculate attenuation coeffiect for a group of photons of a certain energy
double get_attcoe(double energy){
  double attcoe = 393.444 / (pow(energy, 2.87995) + 0.0911984) + 0.0417973;
  return attcoe;
}

//update the photon matrix by replacing the inital photons with the remaing
//photons after a specific interval by calculating the trasmission percentage
//from density, attenuation coeffiect, and the size of the interval
double photons_prime(double height){
  int i;
  for (i=0; i<125; i++){
    int e = photons[i][0];
    double percent = exp(-1 * get_attcoe(e) * average_density(height) * interval);
    photons[i][1] = height + interval;  //update the "iteration-number" column in the matrix
    photons[i][2] *= percent;  //update the "photon-number" column in the matrix
  }
}

int main(){
  FILE * f = fopen("att.dat", "w");
  int h, i, j;
  double start_height = 40000;
  interval = 1000;
  make_photons(start_height);
  for(h=start_height; h<100000; h+=interval){
    for (i=0; i<125; i+=5){
      fprintf(f, "%d %d %d\n", photons[i][0], photons[i][1], photons[i][2]);  
  }
    fprintf(f, "\n");
    photons_prime(h);
  }
  fclose(f);
  return 0;
}