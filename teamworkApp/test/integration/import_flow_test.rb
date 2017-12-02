require 'test_helper'

class ImportFlowTest < ActionDispatch::IntegrationTest
  test "can import data" do 
  	# start on the home page
  	get "/"
  	assert_select "h1", "Teamwork Analysis"

  	# test post method that call python import data
  	csv_upload = fixture_file_upload('files/test_spreadsheet.csv','text/csv')
  	post '/python/importData', params: {file: csv_upload}

  	# check correct redirection
  	assert_response :redirect
  	follow_redirect!
  	assert_response :success
  	assert_select "h1", "Teamwork Analysis"

  	# check for flash notice
  	assert_equal 'Import was successful.', flash[:notice]
  end

  test "cannot import non csv data" do
    # start on the home page
    get "/"
    assert_select "h1", "Teamwork Analysis"

    # test post method with non csv input
    csv_upload = fixture_file_upload('files/.keep','text/csv')
    post '/python/importData', params: {file: csv_upload}

    # check correct redirection
    assert_response :redirect
    follow_redirect!
    assert_response :success
    assert_select "h1", "Teamwork Analysis"

    # check for flash notice
    assert_equal 'Import failed.', flash[:notice]
  end

  test "can delete data" do 
  end
end
