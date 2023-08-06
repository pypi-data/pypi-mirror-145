#=setup=================================================================================================================
# This file provides auxiliary methods to setup catalogue/localstack in a dockerized environment
# and methods by which to also tear the create structs back down.

# This is completed in bash/curl to be as independent as possible from production code, to rule out any issue on our
# side, from regular BAU code changes.

# Needs
# - jq
# - aws
# - curl

# Must have these values exported
# export INTERFACE=""
# export ACCOUNTS=""
# export LOCALSTACK=""
# export LOCALDATA=""   # this is the path where the needed data is for data in new dataset

function setup_named_new_dataset_in_named_new_package_in_named_new_org(){
  LOAD_TYPE=$1
  setup_new_dataset_in_new_package_in_new_org "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" "$9"
} # -> {ORG_SHORTCODE, (ORG_ID, SUBORG_ID), PACKAGE_NAME, PACKAGE_ID,
  #     DATASET_SHORTCODE, DATASET_ID, BUCKET, PREFIX (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)}


function setup_new_dataset_in_new_package_in_new_org(){
  LOAD_TYPE=$1

  if [ -n "$2" ]; then
    ORG_SHORTCODE=$2
  else
    # register a new org with an alpanumeric random name (this step also creates a suborg)
    ORG_SHORTCODE=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
  fi

  if [ -n "$3" ]; then
    PACKAGE_NAME=$3
  else
    # register a package with a random uuid name # todo add multiple under the org
    PACKAGE_NAME=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
  fi

  if [ -n "$4" ]; then
    DATASET_SHORTCODE=$4
  else
    # register a new org with an alpanumeric random name # todo add multiple under each package
    DATASET_SHORTCODE=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
  fi

  if [ -n "$5" ]; then
    BUCKET=$5
  else
    BUCKET=$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 32 | head -n 1)
  fi

  if [ -n "$6" ]; then
    PREFIX=$6
  else
    PREFIX=$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 32 | head -n 1)
  fi

  if [ -n "$7" ]; then
    SQL_ENABLED=$7
  else
    SQL_ENABLED="false"
  fi

  if [ -z $LOAD_TYPE ]; then
    LOAD_STRING="Full Load"
  else
    LOAD_STRING="Incremental Load"
  fi

  if [ -z "$8" ]; then
    setup_org "$ORG_SHORTCODE"
    # allow the user to upload for the ORG_ID/SUBORG_ID just created
  else
    # if you already have an org, you need to pass in the org and suborg for it
    # we assume that the mapping is already done too.
    ORG_ID=$8
    echo "ORG_ID: $ORG_ID"
    SUBORG_ID=$9
    echo "SUBORG_ID: $SUBORG_ID"
    MAPPED="true"
  fi

  if [ "$DEBUG" = "2" ]; then
     echo "Called with:
     LOAD_TYPE: ${LOAD_TYPE}
     ORG_SHORTCODE: ${ORG_SHORTCODE}
     PACKAGE_NAME: ${PACKAGE_NAME}
     DATASET_SHORTCODE: ${DATASET_SHORTCODE}
     BUCKET: ${BUCKET}
     PREFIX: ${PREFIX}
     SQL_ENABLED: ${SQL_ENABLED}
     LOAD_STRING: ${LOAD_STRING}
     ORG_ID: ${8}
     SUBORG_ID: ${9}
     "
  fi

  setup_user_package_creation "$ORG_ID" "$MAPPED"

  data='{
    "data": {
      "attributes": {
        "name":"'$PACKAGE_NAME'",
        "description": "This is a package created for testing S3Proxy.",
        "keywords": ["testing"],
        "topic": "Automotive",
        "access": "Unrestricted",
        "is_internal_within_organisation": false,
        "terms_and_conditions": "There are no terms and conditions",
        "publisher": "b30a3e2c-ad7e-11eb-b02d-377b10141544",
        "suborganisation_id": "'$SUBORG_ID'"
      }
    }
  }'

  output=$(curl -X POST -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
    --data "$data" "http://$INTERFACE/__api_v2/packages/")
  if [ "$DEBUG" = "2" ]; then
    echo "sent: $data"
    echo "package response from catalogue: $output"
  fi
  PACKAGE_ID=$(echo $output | jq -r '.data.id')

  # register s3 data to that dataset
  # we'll add the tests/ folder itself
  export AWS_ACCESS_KEY_ID=test
  export AWS_SECRET_ACCESS_KEY=test

  # to be able to delete a dataset, this bucket must exist else catalogue blows up
  # so we create it here just to make sure that doesnt happen (this is the bucket theu
  # use for data previews)
  aws s3api create-bucket --bucket preview-bucket --endpoint-url="http://$LOCALSTACK" > /dev/null

  # the bucket for the data of this dataset itself
  aws s3api create-bucket --bucket "$BUCKET" --endpoint-url="http://$LOCALSTACK" --region "us-east-1" > /dev/null
  aws s3 cp --recursive --endpoint-url="http://$LOCALSTACK" $LOCALDATA "s3://$BUCKET/$PREFIX/" --quiet

  data='{
    "data":{
      "attributes" : {
        "sql_enabled" : "'$SQL_ENABLED'",
        "earliest_date_field" : "2020",
        "data_preview_type" : "NONE",
        "publishing_frequency" : "Hourly",
        "naming_convention" : "test",
        "documentation": "test",
        "description": "test",
        "content_type": "Structured",
        "data_format": "PARQUET",
        "short_code": "'$DATASET_SHORTCODE'",
        "package_id": "'$PACKAGE_ID'",
        "load_type": "'$LOAD_STRING'",
        "details_visible_to_lite_users": false,
        "has_datafile_monitoring": false,
        "taxonomy": ["Forecasting"],
        "location": {
          "s3" : {
            "type" : "S3",
            "owner": {"aws_account_id": "'$AWS_ACCOUNT_ID'"},
            "bucket" : "'$BUCKET'",
            "prefix": "'$PREFIX'"
          }
        },
        "keywords" : ["test"],
        "name" : "'$DATASET_SHORTCODE'"
      }
    }
  }'
  output=$(curl  -X POST -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
    --data "$data" "http://$INTERFACE/__api_v2/datasets/")
  if [ "$DEBUG" = "2" ]; then
    echo "sent: $data"
    echo "dataset register response from catalogue: $output"
  fi
  DATASET_ID=$(echo $output | jq -r '.data.id')
  echo "package:${PACKAGE_ID}"
  echo "dataset:${DATASET_ID}"
} # -> {ORG_SHORTCODE, (ORG_ID, SUBORG_ID), PACKAGE_NAME, PACKAGE_ID,
  #     DATASET_SHORTCODE, DATASET_ID, BUCKET, PREFIX (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)}

function setup_user_package_creation(){
    USER_ORG_ID=$1
    SET_MAPPINGS=$2

    # TODO Enable after Catalogue DL-7224
    # create new user group underneath org ----------------------------------------------------------------------
#    data = '{
#      "attributes": {
#        "organisation_id": "'$USER_ORG_ID'",
#        "description": "'$USER_ORG_ID'",
#        "name": "'$USER_ORG_ID'",
#        "is_active": true,
#        "is_externally_available": true
#      }
#    }'
#    output=$(curl -X POST -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
#      --data "$data" "http://$INTERFACE/__api_v2/user_groups/")
#    if [ "$DEBUG" = "2" ]; then
#        echo "[DEBUG setup_user_package_creation] user-groups create new group under org: $output"
#    fi
#    NEW_GROUP_ID=$(echo $output | jq -r '.data.id')

    # get the user id ------------------------------------------------------------------------------------------
    # /api/identity/__api_v2/me/  * user_id field, use this in the below
#    output=$(curl -X GET -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
#      "http://$INTERFACE/__api_v2/me/")
#    if [ "$DEBUG" = "2" ]; then
#        echo "[DEBUG setup_user_package_creation] get the user id: $output"
#    fi
#    USER_ID=$(echo $output | jq -r '.datalake.user_id')
#    ADDITIONAL_ORGS_CURRENT=$(echo $output | jq -r '.datalake.additional_organisation_ids')
#    ADDITIONAL_ORGS_NEW=$(echo "$ADDITIONAL_ORGS_CURRENT" | jq ". + [\"$USER_ORG_ID\"]")

    # add user as a new member of the user group ----------------------------------------------------------------
#    data = '{
#      "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
#    }'
#    output=$(curl -X POST -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
#      --data "$data" "http://$INTERFACE/api/identity/__api_v2/user_groups/$NEW_GROUP_ID/members/")
#    if [ "$DEBUG" = "2" ]; then
#        echo "[DEBUG setup_user_package_creation] user-id members: $output"
#    fi

    # add the organisation to the super user as an additional organisation via patch ----------------------------
#    data='{
#        "data": {
#            "attributes": {
#                "additional_organisation_ids": '$ADDITIONAL_ORGS_NEW'
#            }
#        }
#    }'
#    output=$(curl -X PATCH -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
#      --data "$data" "http://$INTERFACE/__api_v2/users/$USER_ID")
#    if [ "$DEBUG" = "2" ]; then
#        echo "[DEBUG setup_user_package_creation] user-id patch: $output"
#    fi
    # me route shows account is added: {"sub": "wmolicki@qa.com", "datalake": {"additional_organisation_ids": ["4c2ed217-1133-4619-81a6-c402e5befa11"], "user_id": "68eda64b-f933-473b-b3ef-4d8e22baa648", "display_name": "w molicki", "organisation_id": "9516c0ba-ba7e-11e9-8b34-000c6c0a981f", "organisation_name": "IHS Markit"}}

    # register aws account for users ----------------------------------------------------------------------------
    AWS_ACCOUNT_ID="$(echo $RANDOM)"
    data='{
        "data": {
            "attributes": {
                "vendor_aws_account_id": "'$AWS_ACCOUNT_ID'",
                "vendor_aws_account_name": "'$AWS_ACCOUNT_ID'",
                "aws_region": "eu-west-1",
                "aws_role_arn": "arn:aws:iam::000000000001:user/root",
                "organisation_id": "'$USER_ORG_ID'"
            }
        }
    }'
    output=$(curl -X POST -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
     --data "$data" "http://$INTERFACE/__api_v2/aws_accounts")
    if [ "DEBUG" = "2" ]; then
      # Performing a modification to allow the user to create packages
      echo "[DEBUG setup_user_package_creation] adding aws_account: $output"
    fi
    ACCOUNT_ID=$(echo $output | jq -r '.data.id')
    if [ "$DEBUG" = "2" ]; then
      echo "AWS_ACCOUNT_ID: ${AWS_ACCOUNT_ID}"
      echo "ACCOUNT_ID: ${ACCOUNT_ID}"
    fi


    # TODO Disable after Catalogue DL-7224
    # get our user group --------------------------------------------------------------------------------------------
    output=$(curl -X GET -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
       "http://$ACCOUNTS/__api_v2/user_groups/")
    GROUP_ID=$(echo $output | jq -r '.data[0].id')
    if [ "$DEBUG" = "2" ]; then
      echo "GROUP_ID: ${GROUP_ID}"
    fi
    NEW_GROUP_ID=$GROUP_ID


    # add the aws_account to our user's group -----------------------------------------------------------------------
    data='{
        "owner_type": "aws-accounts",
        "owner_id": "'$ACCOUNT_ID'",
        "role": "aws-account-user"
    }'
    output=$(curl -s -X POST -H 'Content-Type: application/json'   -H "Authorization: Bearer $JWT" \
       --data "$data" "http://$ACCOUNTS/__api_v2/user_groups/$NEW_GROUP_ID/roles")
    if [ "$DEBUG" = "2" ]; then
      echo "[DEBUG setup_user_package_creation] user-group roles: 'aws-account-user': $output"
    fi

    if [ -z $SET_MAPPINGS ]; then
      # set permissions on suborg for our user now we have the group id -----------------------------------------------
      data='{
        "owner_type": "suborganisations",
        "owner_id":"'$SUBORG_ID'",
        "role": "data-steward"
      }'
      output=$(curl -s -X POST -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
        --data "$data" "http://$ACCOUNTS/__api_v2/user_groups/$NEW_GROUP_ID/roles")
      if [ "$DEBUG" = "2" ]; then
        echo "[DEBUG setup_user_package_creation] user-group roles: 'data-steward': $output"
      fi

      # set permissions on suborganisations with role technical-support for our user ----------------------------------
      data='{
        "owner_type": "suborganisations",
        "owner_id":"'$SUBORG_ID'",
        "role": "technical-support"
      }'
      output=$(curl -s -X POST -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
        --data "$data" "http://$ACCOUNTS/__api_v2/user_groups/$NEW_GROUP_ID/roles")
      if [ "$DEBUG" = "2" ]; then
        echo "[DEBUG setup_user_package_creation] user-group roles: 'technical-support': $output"
      fi

      # set permissions on suborganisations with role access-manager for our user ------------------------------------
      data='{
        "owner_type": "suborganisations",
        "owner_id":"'$SUBORG_ID'",
        "role": "access-manager"
      }'
      output=$(curl -s -X POST -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
        --data "$data" "http://$ACCOUNTS/__api_v2/user_groups/$NEW_GROUP_ID/roles")
      if [ "$DEBUG" = "2" ]; then
        echo "[DEBUG setup_user_package_creation] user-group roles: 'access-manager': $output"
      fi

      # set permissions on suborganisations with role package-creator for our user ----------------------------------
      data='{
        "owner_type": "suborganisations",
        "owner_id":"'$SUBORG_ID'",
        "role": "package-creator"
      }'
      output=$(curl -s -X POST -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
        --data "$data" "http://$ACCOUNTS/__api_v2/user_groups/$NEW_GROUP_ID/roles")
      if [ "$DEBUG" = "2" ]; then
        echo "[DEBUG setup_user_package_creation] user-group roles: 'package-creator': $output"
      fi
    fi
} # -> {NEW_GROUP_ID, SUBORG_ID, USER_ID, AWS_ACCOUNT_ID, ACCOUNT_ID, ADDITIONAL_ORGS_NEW, ADDITIONAL_ORGS_CURRENT}


function setup_org(){
  sc="$1"

  # org --------------------------------------------------------------------------------------------------------
  data='{
    "data": {
      "attributes": {
        "name": "'$sc'",
        "description": "string",
        "external_company_id":"'`uuid`'",
        "is_visible": true,
        "domains": [
          {
            "domain_name": "'$sc'.com"
          }
        ],
        "short_code": "'$sc'"
      }
    }
  }'
  output=$(curl -X POST -H 'Content-Type: application/json'   -H "Authorization: Bearer $JWT" \
      --data "$data" "http://$ACCOUNTS/__api_v2/organisations")
  if [ "$DEBUG" = "2" ]; then
      echo "[DEBUG setup_org] organisations: $output"
  fi
  ORG_ID=$(echo $output | jq -r '.data.id')

  if [ "$DEBUG" = "2" ]; then
      echo "[DEBUG setup_org] ORG_ID: ${ORG_ID}"
  fi

  # suborg ----------------------------------------------------------------------------------------------------
  data='{
    "data": {
      "attributes": {
        "name": "'$sc'_sub",
        "description": "string",
        "organisation_id": "'$ORG_ID'"
      }
    }
  }'
  output=$(curl -X POST -H 'Content-Type: application/json'   -H "Authorization: Bearer $JWT" \
      --data "$data" "http://$ACCOUNTS/__api_v2/suborganisations")
  if [ "$DEBUG" = 2 ]; then
      echo "[DEBUG setup_org] suborganisations: $output"
  fi

  SUBORG_ID=$(echo $output | jq -r '.data.id')
  if [ "$DEBUG" = "2" ]; then
      echo "[DEBUG setup_org] SUBORG_ID: ${SUBORG_ID}"
  fi
} # -> {ORG_ID, SUBORG_ID}

#=teardown==============================================================================================================


function teardown_org_by_id(){
  output=$(curl -X GET -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
      "http://$ACCOUNTS/__api_v2/me/")
  if [ "$DEBUG" = "2" ]; then
      echo "[DEBUG teardown_org_by_id] me: $output"
  fi

  USER_ID=$(echo $output | jq -r '.datalake.user_id')
  if [ "$DEBUG" = "2" ]; then
      echo "[DEBUG teardown_org_by_id] USER_ID: $USER_ID"
  fi

  # TODO Enable after Catalogue DL-7224
  # restore original additional_orgs field of the user, unattach the additional org
  # add the organisation to the super user as an additional organisation via patch ----------------------------
#  data='{
#      "data": {
#          "attributes": {
#              "additional_organisation_ids": "'$ADDITIONAL_ORGS_CURRENT'"
#          }
#      }
#  }'
#  output=$(curl -X PATCH -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
#      --data "$data" "http://$INTERFACE/__api_v2/users/$USER_ID")
#  if [ "$DEBUG" = "2" ]; then
#      echo "[DEBUG teardown_org_by_id] reversed user-id patch: $output"
#  fi

  # remove user from group -----------------------------------------------------------------------------------
#  output=$(curl -X DELETE -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
#      "http://$INTERFACE/__api_v2/user_groups/$NEW_GROUP_ID/members/$USER_ID")
#  if [ "$DEBUG" = "2" ]; then
#      echo "[DEBUG teardown_org_by_id] user-groups create new group under org: $output"
#  fi
#  NEW_GROUP_ID=$(echo $output | jq -r '.data.id')
#  if [ "$DEBUG" = "2" ]; then
#      echo "[DEBUG teardown_org_by_id] NEW_GROUP_ID: $NEW_GROUP_ID"
#  fi

  # delete user group ---------------------------------------------------------------------------------------
  #  output=$(curl -X DELETE -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
  #    "http://$INTERFACE/__api_v2/user_group/$NEW_GROUP_ID")
  #  if [ "$DEBUG" = "2" ]; then
  #      echo "delete user group $output"
  #  fi


  # delete the org ------------------------------------------------------------------------------------------
  org_id=$1
  output=$(curl -X DELETE -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
      "http://$ACCOUNTS/__api_v2/organisations/${org_id}")
  if [ "$DEBUG" = "2" ]; then
      echo "[DEBUG teardown_org_by_id] delete org: $output"
  fi
}


function teardown_suborg_by_id(){
    suborg_id=$1
    output=$(curl -X DELETE -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
        "http://$ACCOUNTS/__api_v2/suborganisations/${suborg_id}")
    if [ "$DEBUG" = "2" ]; then
        echo "[DEBUG teardown_suborg_by_id] delete suborg_id: $output"
    fi
}


function teardown_package_by_id(){
    package_id=$1
    output=$(curl -X DELETE -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
        "http://$INTERFACE/__api_v2/packages/${package_id}")
    if [ "$DEBUG" = "2" ]; then
        echo "[DEBUG teardown_package_by_id] delete package_id: $output"
    fi
}


function teardown_dataset_by_id(){
    dataset_id=$1
    output=$(curl -X DELETE -H 'Content-Type: application/json' -H "Authorization: Bearer $JWT" \
        "http://$INTERFACE/__api_v2/datasets/${dataset_id}")
    if [ "$DEBUG" = "2" ]; then
        echo "[DEBUG teardown_dataset_by_id] delete dataset_id: $output"
    fi
}


function teardown_s3_content(){
  bucket=$1
  prefix=$2
  export AWS_ACCESS_KEY_ID=test
  export AWS_SECRET_ACCESS_KEY=test
  aws s3 rm "s3://$bucket/$prefix" --recursive --endpoint-url="http://$LOCALSTACK" --quiet
}
