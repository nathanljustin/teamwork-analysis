Rails.application.routes.draw do

  root 'high_voltage/pages#show', id: 'home'
  get '/student_graph/show'
  post '/student_graph/graph', as: 'selections'
  post '/python/importData/' => 'python#importData'
  get '/python/overallBar/' => 'python#overallBar'
  get '/overallBar/' => 'high_voltage/pages#show', id: 'overallshow'
  get '/importData/' => 'high_voltage/pages#show', id: 'importdata'

end
