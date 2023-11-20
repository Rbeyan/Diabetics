import atexit
import os
import logging

from dotenv import load_dotenv
from datetime import date
from pathlib import Path

from kld7radar.binary_file_reader import BinaryFileReader
from kld7radar.consumer import Consumer, StorageMethods
from kld7radar.radar import Radar, RadarConfigReader

from kld7radar.replay_writer import ReplayWriter
from optparse import OptionParser

ROOT_PATH = Path(__file__).parent.parent


def run_radar(serial_port: str,
              fps: int,
              activated_sampling_method: str,
              storage_method: str,
              storage_server_ip: str,
              host_ip: str,
              location: str,
              samples_per_save: int):
    if StorageMethods(storage_method):
        logging.info(f"Starting radar...")
        logging.info(f"Using RADAR_STORAGE_METHOD=\"{storage_method}\"")
        logging.info(f"Using RADAR_SAMPLING_METHOD=\"{activated_sampling_method}\"")

    radar = Radar(serial_port)

    # do not delete this line: ensure that we always properly disconnect the radar.
    # Without doing this, weird runtime behaviors might occur, when running the radar the next time
    atexit.register(radar.disconnect)

    logging.info(f"Connecting to serial port {serial_port}...")
    radar.connect()
    logging.info("Connection to radar established.")

    if not radar.is_running():
        logging.info('Error during initialisation for K-LD7')

    logging.info("Setting radar parameters...")

    radar_config_path = os.path.join(ROOT_PATH, "radar_config.json")
    radar_config = RadarConfigReader.read(radar_config_path)
    radar.set_parameters(config=radar_config)

    radar_params = radar.get_parameters()
    logging.info("Params after initialization: ")
    logging.info(radar_params)

    logging.info("Parameters set.")

    logging.info(f"Running sampling method {activated_sampling_method} at {fps} FPS")

    logging.info("Start streaming measurements...")
    Consumer(
        identifier="1",
        radar=radar,
        fps=fps,
        activated_sampling_method=activated_sampling_method,
        storage_method_name=storage_method,
        storage_server_ip=storage_server_ip,
        host_ip=host_ip,
        location=location,
        samples_per_save=samples_per_save
    ).read_stream()

    radar.disconnect()


def extract_replay_data(replay_filepath: str) -> None:
    base_name = os.path.basename(replay_filepath).replace('.bin', '')

    binary_radar_file_reader = BinaryFileReader(replay_filepath)
    samples, settings = binary_radar_file_reader.read()

    replay_writer = ReplayWriter(samples, settings)
    replay_writer.write_samples(filename=base_name)


def main():
    parser = OptionParser()
    parser.add_option(
        "-r",
        "--read-replay",
        dest="replay_filepath",
        help="Read and process a replay file",
        metavar="FILE"
    )

    parser.add_option(
        "-q",
        "--quiet",
        action="store_false",
        dest="verbose",
        default=True,
        help="Do not print status messages to stdout"
    )

    (options, args) = parser.parse_args()

    today = date.today()
    current_date = today.strftime("%d_%m_%y")
    log_path = os.path.join(ROOT_PATH, 'logs', f"status_{current_date}.log")
    log_handlers = [
        logging.FileHandler(log_path, mode="a", encoding="utf8"),
    ]

    if options.verbose:
        log_handlers.append(
            logging.StreamHandler()
        )

    logging.basicConfig(
        handlers=log_handlers,
        format="%(asctime)s.%(msecs)03d|%(levelname)s|%(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        level=logging.DEBUG
    )

    if options.replay_filepath:
        logging.info(f"Processing replay file {options.replay_filepath}")
        extract_replay_data(replay_filepath=options.replay_filepath)
    else:
        load_dotenv()
        serial_port = os.getenv("RADAR_SERIAL_PORT")
        fps = int(os.getenv("RADAR_FPS"))
        activated_sampling_method = os.getenv("RADAR_SAMPLING_METHOD")
        storage_method = os.getenv("RADAR_STORAGE_METHOD")
        storage_server_ip = os.getenv("RADAR_STORAGE_SERVER_URL")
        host_ip = os.getenv("RADAR_HOST_IP")
        location = os.getenv("RADAR_LOCATION")
        samples_per_save = int(os.getenv("RADAR_SAMPLES_PER_SAVE"))
        run_radar(
            serial_port=serial_port,
            fps=fps,
            activated_sampling_method=activated_sampling_method,
            storage_method=storage_method,
            storage_server_ip=storage_server_ip,
            host_ip=host_ip,
            location=location,
            samples_per_save=samples_per_save
        )


if __name__ == '__main__':
    main()
