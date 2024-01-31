param location string = resourceGroup().location
param storageAccountName string = 'publictest${uniqueString(resourceGroup().id)}'
param blobContainerName string = 'testcontainer'

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: true
  }

  resource blobService 'blobServices' existing = {
    name: 'default'
  }
}

resource blobContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  name: blobContainerName
  parent: storageAccount::blobService
  properties: {
    publicAccess: 'Container'
  }
}
