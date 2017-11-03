Rails.application.routes.draw do
  root 'high_voltage/pages#show', id: 'home'
<<<<<<< HEAD
  resources :python do
    collection do
      get :overallPie
    end
  end
=======
  get '/python/studentGraph/' => "python#studentGraph"  
  get '/python/overallBar/' => 'python#overallBar'
  get '/studentGraph/' => 'high_voltage/pages#show', id: 'studentshow'
  get '/overallBar/' => 'high_voltage/pages#show', id: 'overallshow'
>>>>>>> 8eb5a02c5f819de06edcac64304b2844cc0e8830
end
