Rails.application.routes.draw do


  root 'high_voltage/pages#show', id: 'home'

  post '/python/importData/' => 'python#importData'

  get '/python/studentGraph/' => "python#studentGraph"  
  get '/python/overallBar/' => 'python#overallBar'
  get '/python/deleteData/' => 'python#deleteData'
  get '/studentGraph/' => 'high_voltage/pages#show', id: 'studentshow'
  get '/overallBar/' => 'high_voltage/pages#show', id: 'overallshow'
  get '/importData/' => 'high_voltage/pages#show', id: 'importdata'


end
