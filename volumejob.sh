#!/bin/bash

ls data/json_input/*.json | parallel --jobs 32 bosh exec launch -s zenodo.4043546 ./{}