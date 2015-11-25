# Azure management for Debian

Tools for managing images within the Microsoft Azure platform, primarily for Debian.

## Requirements

* Python >= 3.4
* azure-servicemanagement-legacy
* azure-storage
* pyyaml
* py.test

## Commands

### Build image: `azure_build_image`

Build a Debian image according to the specified section within the config.

### Delete image: `azure_delete_image`

Delete existing image from Azure.

### Upload image: `azure_upload_image`

Upload new image to Azure.

### List images: `azure_list_images`

List all matching images.

### Extract publishsettings file: `azure_extract_publishsettings`

## Config

Example config for all Debian distributions.

    ---
    default: &DEFAULT
      storage_account: null
      storage_container: null
      subscription: null
      subscription_keyfile: null
    
    default-daily: &DEFAULT-DAILY
      <<: *DEFAULT
      image_name: 'Debian-{release_number}-DAILY-amd64-{timestamp}'
      image_label: 'Debian {release_number} "{release_name}" DAILY'
    
    wheezy:
      <<: *DEFAULT-DAILY
      release: wheezy
      release_name: Wheezy
      release_number: 7
    
    jessie:
      <<: *DEFAULT-DAILY
      release: jessie
      release_name: Jessie
      release_number: 8
    
    stretch:
      <<: *DEFAULT-DAILY
      release: stretch
      release_name: Stretch
      release_number: 9
