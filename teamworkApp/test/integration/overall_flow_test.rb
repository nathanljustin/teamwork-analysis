require 'test_helper'

class OverallFlowTest < ActionDispatch::IntegrationTest
  test "overall with no data" do 
  	# start on the home page
  	get "/"
  	assert_select "h1", "Teamwork Analysis"

  	# move to overall distribution
  	get "/overallBar/"
  	assert_select "h1", "Overall Distribution"
  	assert_select "h2", "Understanding Styles"
  end

  test "overall after data import" do 
  	# start on the home page
  	get "/"
  	assert_select "h1", "Teamwork Analysis"

    # add data and move back to main page
    csv_upload = fixture_file_upload('files/.keep','text/csv')
    post '/python/importData', params: {file: csv_upload}
    assert_response :redirect
    follow_redirect!
    assert_response :success
    assert_select "h1", "Teamwork Analysis"

  	# move to overall distribution
  	get "/overallBar/"
  	assert_select "h1", "Overall Distribution"
  	assert_select "h2", "Understanding Styles"
  end

  test "overall after deleting data" do 
  	# start on the home page
  	get "/"
  	assert_select "h1", "Teamwork Analysis"

    # add data and move back to main page
    csv_upload = fixture_file_upload('files/.keep','text/csv')
    post '/python/importData', params: {file: csv_upload}
    assert_response :redirect
    follow_redirect!
    assert_response :success
    assert_select "h1", "Teamwork Analysis"

    # delete data and move back to main page
    post '/python/deleteData'
    assert_response :redirect
    follow_redirect!
    assert_response :success
    assert_select "h1", "Teamwork Analysis"

  	# move to overall distribution
  	get "/overallBar/"
  	assert_select "h1", "Overall Distribution"
  	assert_select "h2", "Understanding Styles"
  end
end
