resource "aviatrix_account" "azure" {
  account_name        = "$account_name"
  cloud_type          = 8
  arm_subscription_id = "$ARM_SUBSCRIPTION_ID"
  arm_directory_id    = "$ARM_TENANT_ID"
  arm_application_id  = "$ARM_CLIENT_ID"
  arm_application_key = $ARM_CLIENT_SECRET
}

$s3_backend