#!/bin/bash
set -e

pg_restore -U $POSTGRES_USER --no-owner --no-privileges -d marketplace ../db.dump
