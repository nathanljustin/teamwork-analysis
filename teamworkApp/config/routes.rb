Rails.application.routes.draw do

  root 'high_voltage/pages#show', id: 'home'
  get '/student_graph/show'
  post '/student_graph/show' => 'student_graph#graph'
  get '/overall/show'
  post '/overall/show' => 'overall#graph'
  post '/python/importData/' => 'python#importData'
  post '/python/deleteData/' => 'python#deleteData'
  get '/importData/' => 'high_voltage/pages#show', id: 'importdata'
end
