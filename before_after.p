
set title font ',13'
set key font ',13'
set border lw 1.4
set xtics 0,10,120 font ',13'
set ytics font ',13'
set grid
set xrange [0:125]




set title "Initial vs. Final Distribution of Photons after\nAttenuation through the Atmosphere"
set xlabel 'Photon Energy (keV)' font ',13'
set ylabel 'Photon Intensity' font ',13'
plot 'before_after.dat' u 1:($2/10) w l lw 3 title 'Initial Distribution', 'before_after.dat' u 1:($3/10) w l lw 3 title 'Final Distribution'
pause -1 "Press the enter key to continue"
