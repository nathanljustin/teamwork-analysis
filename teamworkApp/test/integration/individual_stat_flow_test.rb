require 'test_helper'

class IndividualStatFlowTest < ActionDispatch::IntegrationTest
  test "individual with data" do 
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

  	# move to individual students page
  	get student_graph_show_path
  	assert_select "h1", "Individual Statistics"
  	assert_select "h2", "What Makes an Effective Team?"
  end
end
