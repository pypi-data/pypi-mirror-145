###############################################################################
# Copyright (C) 2022 Habana Labs, Ltd. an Intel Company
# All Rights Reserved.
#
# Unauthorized copying of this file or any element(s) within it, via any medium
# is strictly prohibited.
# This file contains Habana Labs, Ltd. proprietary and confidential information
# and is subject to the confidentiality and license agreements under which it
# was provided.
#
###############################################################################
def habana_imagenet_dataset(fallback,
                            is_training,
                            tf_data_dir,
                            jpeg_data_dir,
                            batch_size,
                            num_channels,
                            img_size,
                            dtype,
                            use_distributed_eval,
                            **fallback_kwargs):
    return fallback(is_training=is_training,
                    data_dir=tf_data_dir,
                    batch_size=batch_size,
                    dtype=dtype,
                    use_distributed_eval=use_distributed_eval,
                    **fallback_kwargs)
