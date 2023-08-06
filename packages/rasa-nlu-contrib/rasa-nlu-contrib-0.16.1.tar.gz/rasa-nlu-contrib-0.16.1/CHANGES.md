# Changes

## 0.16.1 (2022-04-05)
- Fix issue with `server` dependency

## 0.16.0 (2021-01-21)
- Minimize the bare installation
  * server (HTTP) can be installed now separately
- Rasa-NLU version 0.15.1
- Known issues:
  * Tests
    + tests/base/test_extractors.py :: 1 failing tests due Python version
    + tests/base/test_featurizers.py :: 4 failing tests due Python version
    + tests/base/test_multitenancy.py :: 5 failing tests due Python version
    + tests/training/test_train.py :: 5 failing tests due Python version
  * Requirements
    + `tox` is not used due to dependecy issue on `six`

## 0.15.1 (2021-01-20)
- Initial release
- Rasa-NLU version 0.15.1
- Known issues:
  * tests/base/test_extractors.py :: 1 failing tests due Python version
  * tests/base/test_featurizers.py :: 4 failing tests due Python version
  * tests/base/test_multitenancy.py :: 5 failing tests due Python version
  * tests/training/test_train.py :: 5 failing tests due Python version
