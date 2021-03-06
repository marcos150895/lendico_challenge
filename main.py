# -*- coding: utf-8 -*-

import gc

from extractors.riotgames.riot_extractor import RiotExtractor
from config.command_line_args import CommandLineArgs
from writers.writer import Writer
from analysis.riot_champion_points_x_champion_id import RiotChampionPointsXChampionID
from helpers.utils import Utils


# enable garbage collector
gc.enable()

# get configs
confs = CommandLineArgs().get_args()


def master_leagues():
    endpoint = confs.master_leagues_endpoint
    headers = Utils.format_header(confs.access_key)

    master_leagues_json = RiotExtractor()\
        .get_data_from_api(endpoint=endpoint, headers=headers, api_name='master leagues')

    return master_leagues_json


def champion_mastery():
    endpoint_without_slash_in_the_end = Utils.remove_slash_in_end_of_string(confs.champion_mastery_endpoint)
    endpoint = endpoint_without_slash_in_the_end + '/' + confs.champion_mastery_summoner_id
    headers = Utils.format_header(confs.access_key)

    champion_mastery_json = RiotExtractor()\
        .get_data_from_api(endpoint=endpoint, headers=headers, api_name='champion mastery')

    return champion_mastery_json


def main():
    # checking if output path exists
    Utils.create_path_if_not_exists(confs.dest)

    # executing master leagues json writer
    master = master_leagues()
    champion = champion_mastery()

    # writer both in file system
    Writer().write_json(data=master, file_name="master_leagues", output_path=confs.dest)
    Writer().write_json(data=champion, file_name="champion_mastery", output_path=confs.dest)

    # plotting and save championPointchart
    RiotChampionPointsXChampionID(champion).save_chart_as_image(path=confs.dest)


if __name__ == '__main__':
    main()
