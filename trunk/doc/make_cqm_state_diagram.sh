#!/bin/bash

./sm2dot $1 | dot -Tpdf > $2
