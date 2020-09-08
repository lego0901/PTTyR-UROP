#  TORCH API 명세 리스트

### descriptions/woosung

  - basics.pdf
    - size, stride, shape, tensor
    - range, arange, linspace
    - zeros, empty, rand, randn, randint, randperm, full, normal, new_empty, new_full, clone
    - zeros_like, empty_like, rand_like, randn_like, full_like
    - scalar_tensor, eye
    - round, floor, ceil, exp, log, log10, log2, log1p, sigmoid, sqrt, rsqrt, cos, sin, tan, angle, sign, neg, frac, contiguous, clamp
    - threshold, softmax, log_softmax, inverse, flip
    - eq, le, lt, ge, gt, mul, div, fmod, atan2, add, sub, pow
    - item, view
    - expand, split, chunk
    - nonzero
  - nontensor.pdf
    - numel, dim, ndim, ndimension, eq(torch.Tensor.eq와 서로 다름)
    - tolist, as_tensor, from_numpy
  - statistics.pdf
    - max, min
    - sum, mean, prod, norm
    - all, any
    - var, std, mode, median
    - sort
  - signals.pdf
    - stft, rfft, fft
    - hann_window, bartlett_window, hamming_window
    - svd, diag
    - bilinear
  - simple_neural.pdf
    - Linear
    - ReLU, ReLU6, relu
    - CrossEntropyLoss, TripletMarginLoss(Not Done)
    - Dropout, dropout
    - Sequential
  - convolutionals.pdf
    - Conv2d, conv2d, Conv1d, conv1d, Conv3d, conv3d
    - ConvTranspose1d, conv_transpose1d, unfold
    - MaxPool2d, max_pool2d, max_pool2d_with_indices, AvgPool2d, AdaptiveAvgPool2d, AdaptiveAvgPool3d
    - BatchNorm2d, BatchNorm3d, BatchNorm1d, batch_norm, GroupNorm
  - recurrents.pdf
      - RNN, LSTM, GRU
      - Embedding, EmbeddingBag, embedding



### descriptions/junhyeok

- argmax, cumsum, dot, expand_as, isfinite, isnan, real, take, detach, is\_signed, topk, unbind
- random\_, bernoulli\_, clamp\_, fill\_, masked\_fill\_, normal\_, random\_, uniform\_. unsqueeze\_, zero\_, 



### descriptions/kyuyeon

- flatten, ones, squeeze, triu, unsqueeze

