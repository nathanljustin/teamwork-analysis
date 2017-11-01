Rails.application.routes.draw do
  root 'high_voltage/pages#show', id: 'home'
  resources :python do
    collection do
      get :overallPie
    end
  end
end
