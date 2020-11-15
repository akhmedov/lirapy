import sys, argparse
from linear import plot_ex_vs_hz, plot_hz_numerical, plot_sinc_furier_zone, plot_ex_from_time
from process import compute_observer
from visual import show_port_location, show_prob_data
from cst_data import OBSERVERS, Antenna, observer


def run_plot_tests():

	"""
	TODO: documentation by Denis
	"""

	plot_ex_vs_hz()
	plot_hz_numerical()
	plot_sinc_furier_zone()
	plot_ex_from_time()
	show_port_location()
	show_prob_data()


def main():

	"""
	TODO: documentation by Denis
	"""

	about = 'Visualization and computing for nonliner filed propagation from LIRA'
	parser = argparse.ArgumentParser(description=about)
	obs_help = 'Position of observer to compute nonlinear field'
	parser.add_argument('--observer', action='store',type=int, help=obs_help, required=False)
	obslist_help = 'Show available observers position'
	parser.add_argument('--obslist', action='store_true', help=obslist_help, required=False)
	geometry_help = 'Show antenna geometry'
	parser.add_argument('--geometry', action='store_true', help=geometry_help, required=False)
	plottest_help = 'Runs some visual tests'
	parser.add_argument('--test', action='store_true', help=plottest_help, required=False)
	help_ratio = 'Position of observer to compute nonlinear field'
	parser.add_argument('--ratio', action='store',type=int, help=help_ratio, required=False, default=0)
	args = parser.parse_args()


	if args.obslist:
		for i in range(OBSERVERS):
			obs = observer(i+1)
			print('Observer', i+1, '=', obs.x, obs.y, obs.z)

	if args.geometry:
		print('Total length: ', Antenna.bigradius + Antenna.focuslength)
		print('Aperture radius: ', Antenna.apperture)

	if args.test:
		run_plot_tests()

	if args.observer:
		if 0 < args.observer > OBSERVERS:
			print('[EE] The observer ID is not valid!')
			parser.print_help()
			sys.exit()
		compute_observer(args.observer, args.ratio)

	if len(sys.argv) == 1:
		parser.print_help(sys.stderr)
		sys.exit(1)


if __name__  == '__main__':
	main()
