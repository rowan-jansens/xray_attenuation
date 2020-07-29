set pm3d
set pal grey
set grid
set yrange [0:125]
set ytics 0,20,125 font ',13'
set xtics font ',13'
set ztics font ',13'
set key font ',13'
set title font ',13'
set border lw 1.4
set title "Attenuation of X-Rays Through the Upper Atmosphere \n {/*0.9 From a High-Altitude Nuclear Explosion}"
set ylabel 'Photon Energy (keV)' rotate parallel font ',13'
set xlabel 'Altitude (km)' rotate parallel font ',13'
set zlabel 'Photon Intensity' rotate parallel font ',13'
splot 'surface_evolution.dat' u ($1/1000):2:($3/10) w l lw 0.5 lc black title 'Attenuation'
pause -1 "Press the enter key to continue"
