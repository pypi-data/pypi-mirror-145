from multiprocessing import Pool
from tqdm import tqdm
import cameo_claw.istarmap

cameo_claw.istarmap.ignore_no_use_warning()


def it_mp_f(f, tup_param):
    int_progress = 0
    with Pool(25) as p:
        # disable=True
        for url in tqdm(p.istarmap(f, tup_param), total=len(tup_param)):
            int_progress += 1
            yield int_progress, url
