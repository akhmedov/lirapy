import os
import sys
import argparse
from linear import plot_ex_vs_hz, plot_hz_numerical, plot_sinc_furier_zone, plot_ex_from_time
from interpol import time_sync
from visual import show_port_location, show_prob_data


def run_plot_tests():
	plot_ex_vs_hz()
	# plot_hz_numerical()
	# plot_sinc_furier_zone()
	plot_ex_from_time()
	show_port_location()
	show_prob_data()


def main():
	about = 'Visualization and computing for nonliner filed propagation from LIRA'
	parser = argparse.ArgumentParser(description=about)
	parser.add_argument('compute', action='store', help=' ')
	args = parser.parse_args()


if __name__  == '__main__':
	run_plot_tests()
