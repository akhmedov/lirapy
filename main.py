import os
import sys
import argparse
from linear import plot_ex_vs_hz, plot_hz_numerical, plot_sinc_furier_zone, plot_ex_from_time
from interpol import time_sync, compute_observer
from visual import show_port_location, show_prob_data
from cst_data import OBSERVERS, PORTS

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
	obs_help = 'Position of observer to compute nonlinear field'
	parser.add_argument('--observer', action='store',type=int, help=obs_help, required=False)
	obslist_help = 'Show available observers position'
	parser.add_argument('--obslist', action='store_true', help=obslist_help, required=False)
	args = parser.parse_args()

	if args.obslist:
		for i in range(OBSERVERS):
			obs = observer(i+1)
			print('Observer', i+1, '=', obs.x, obs.y, obs.z)

	if args.observer:
		# TODO: chack is args.observer valid
		compute_observer(args.observer)


if __name__  == '__main__':
	# run_plot_tests()
	main()
