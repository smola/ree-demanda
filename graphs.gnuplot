
set xdata time
set timefmt '%Y%m'

set terminal postscript enhanced color solid lw 3 "Times-Roman" 20
set output "graphs/monthly_absolute.ps"

set xrange ["20070101":"20130828"]

set key top right

plot [:][:] \
  'graph_data/full_monthly_autoproduction.dat' using 1:2 title "autoproduction" with lines, \
  'graph_data/full_monthly_coal.dat' using 1:2 title "coal" with lines, \
  'graph_data/full_monthly_combined_cycle.dat' using 1:2 title "combined cycle" with lines, \
  'graph_data/full_monthly_eolic.dat' using 1:2 title "eolic" with lines, \
  'graph_data/full_monthly_solar.dat' using 1:2 title "solar" with lines, \
  'graph_data/full_monthly_fuel_gas.dat' using 1:2 title "fuel/gas" with lines, \
  'graph_data/full_monthly_hydroelectric.dat' using 1:2 title "hydroelectric" with lines, \
  'graph_data/full_monthly_nuclear.dat' using 1:2 title "nuclear" with lines, \
  'graph_data/full_monthly_international_exchange.dat' using 1:2 title "international exchange" with lines, \
  'graph_data/full_monthly_balearic_link.dat' using 1:2 title "balearic link" with lines

set output "graphs/monthly_relative.ps"

set yrange [-0.2:1]

plot [:][:] \
  'graph_data/full_monthly_pct_autoproduction.dat' using 1:2 title "autoproduction" with lines, \
  'graph_data/full_monthly_pct_coal.dat' using 1:2 title "coal" with lines, \
  'graph_data/full_monthly_pct_combined_cycle.dat' using 1:2 title "combined cycle" with lines, \
  'graph_data/full_monthly_pct_eolic.dat' using 1:2 title "eolic" with lines, \
  'graph_data/full_monthly_pct_solar.dat' using 1:2 title "solar" with lines, \
  'graph_data/full_monthly_pct_fuel_gas.dat' using 1:2 title "fuel/gas" with lines, \
  'graph_data/full_monthly_pct_hydroelectric.dat' using 1:2 title "hydroelectric" with lines, \
  'graph_data/full_monthly_pct_nuclear.dat' using 1:2 title "nuclear" with lines, \
  'graph_data/full_monthly_pct_international_exchange.dat' using 1:2 title "international exchange" with lines, \
  'graph_data/full_monthly_pct_balearic_link.dat' using 1:2 title "balearic link" with lines


