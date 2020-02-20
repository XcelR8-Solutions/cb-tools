#!/bin/bash
#
# Task - Echo out of variables 
#
echo "Morpheus Variables"
echo "-----------------------------"
echo "Instance Name: <%= instance.name %>"
echo "Instance Plan: <%= instance.plan %>"
echo "External IP: <%= server.externalIp %>"
echo "Date Created: <%= server.dateCreated %>"
echo "API Key: <%= server.apiKey %>"
echo "Agent Version: <%= server.agentVersion %>"
