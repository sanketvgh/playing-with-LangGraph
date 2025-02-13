# import module_1.chains
# import module_1.router
# import module_1.agent
# import module_1.agent_github_username
# from configs.settings import settings
# import module_1.simple_graphs
import time
import cProfile
import pstats
# from module_1.agent_with_memory import run
# from module_2.state_schema import run
# from module_2.state_schema_pydantic import run
# from module_2.state_reducers import run
from module_2.state_reducers_custom import run
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def profile_execution(func):
    def wrapper(*args, **kwargs):
        with cProfile.Profile() as pr:
            result = func(*args, **kwargs)
            stats = pstats.Stats(pr)
            stats.sort_stats(pstats.SortKey.TIME)
            stats.dump_stats(filename=f"{func.__name__}_profile.prof")
            return result
    return wrapper


def time_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        logger.debug(f"Execution time: {end_time - start_time} seconds")
        return result
    return wrapper


@time_execution
def main():
    run()


if __name__ == "__main__":
    main()
