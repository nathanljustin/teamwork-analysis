Rails.application.routes.draw do
  root 'high_voltage/pages#show', id: 'home'
  get '/python/studentGraph/' => "python#studentGraph"  
  get '/python/overallBar/' => 'python#overallBar'
  get '/python/importData/' => 'python#importData'
  get '/studentGraph/' => 'high_voltage/pages#show', id: 'studentshow'
  get '/overallBar/' => 'high_voltage/pages#show', id: 'overallshow'
  get '/importData/' => 'high_voltage/pages#show', id: 'home'
end
