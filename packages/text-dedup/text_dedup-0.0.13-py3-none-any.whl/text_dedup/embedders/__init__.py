#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date         : 2021-06-05 14:51:48
# @Author       : Chenghao Mou (mouchenghao@gmail.com)

"""Embedding models for text."""

from typing import Any, List, Union

import numpy as np


class Embedder:

    def embed(self, corpus: List[Any]) -> Union[np.ndarray, List[int], List[np.ndarray], List[slice]]:
        """Embed a corpus.

        Parameters
        ----------
        corpus : List[Any]
            Corpus to embed.

        Returns
        -------
        np.ndarray
            Embedding of the corpus.
        """
        raise NotImplementedError