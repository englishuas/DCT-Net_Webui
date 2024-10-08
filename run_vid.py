import cv2, argparse
import imageio
from tqdm import tqdm
import numpy as np
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

def process(args):
    model_name = args.model_name

    reader = imageio.get_reader(args.video_path)
    fps = reader.get_meta_data()['fps']
    writer = imageio.get_writer(args.save_path, mode='I', fps=fps, codec='libx264')


    img_cartoon = pipeline(Tasks.image_portrait_stylization, model=model_name)

    for _, img in tqdm(enumerate(reader)):
        result = img_cartoon(img[..., ::-1])
        res = result[OutputKeys.OUTPUT_IMG]
        writer.append_data(res[..., ::-1].astype(np.uint8))
    writer.close()
    print('finished!')
    print('result saved to %s'% args.save_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_path', type=str,required=True)
    parser.add_argument('--save_path', type=str, default='res.mp4')
    parser.add_argument('--model_name', type=str,required=True)

    args = parser.parse_args()

    process(args)
