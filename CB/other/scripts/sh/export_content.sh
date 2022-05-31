#!/bin/sh

ENTITY=""
ENTITY_NAME=""
GIT_USERNAME=""
GIT_EMAIL=""
GIT_PAT=""
PROCEED="no"

echo ""
echo "----------------------------------------------"
echo "| Bundles up and submits content              "
echo "|                                             "
echo "| Item you are checking in options:           "
echo "| ---------------------------------           "
echo "| - blueprint                                 "
echo "| - ui extension                              "
echo "| - orchestration action                      " 
echo "| - server action                             "
echo "| - recurring job                             "
echo "| - rule                                      "
echo "|                                             "
echo "----------------------------------------------"
echo ""

# 1. Get entity to check-in
echo "What are you contributing [blueprint|ui extension|orchestration action|resource action|server action|recurring job|rule]?" 
read ENTITY

# 2. Get entity name
echo "What are you name of the $ENTITY (enclose in quotes if spaces)?" 
read ENTITY_NAME

# 3. Get git username
echo "What is your git username?" 
read GIT_USERNAME

# 4. Get git email
echo "What is your git email?"
read GIT_EMAIL

# 5. Get git PAT
echo "What is your git PAT (Personal Access Token)?" 
read GIT_PAT

# 6. Print summary
echo ""
echo "----------------------------------------------"
echo "| Summary:                                    "
echo "| --------                                    "
echo "| Submitting - $ENTITY                        "
echo "| Name - $ENTITY_NAME                         "
echo "| GIT Username - $GIT_USERNAME                "
echo "| GIT Email - $GIT_EMAIL                      "
echo "|                                             "
echo "----------------------------------------------"
echo ""

# 7. Proceed?
echo "Proceed (yes/no)?"
read PROCEED

if [ $PROCEED == 'yes' ]
then 
	echo "Running check-in process"
	/opt/cloudbolt/manage.py export_content "$ENTITY" "$ENTITY_NAME" -a $GIT_USERNAME $GIT_EMAIL $GIT_PAT -b poc_artifacts
else
	echo "NOT Proceeding, user said no soup for you!"
fi

