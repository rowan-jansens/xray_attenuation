set pm3d
set pal grey
set grid
set title "Attenuation of X-Rays Through the Upper Atmosphere \n {/*0.9 From a High-Altitude Nuclear Explosion}"
set xlabel 'Photon Energy (keV)' rotate parallel
set ylabel 'Altitude (km)' rotate parallel
set zlabel 'Photons' rotate parallel
splot 'att.dat' u 1:($2/1000):3 w l lw 0.5 lc black title 'Attenuation'
pause -1 "Press the enter key to continue"
