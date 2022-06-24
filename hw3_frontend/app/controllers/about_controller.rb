require 'csv'
class AboutController < ApplicationController
    def index
        system("open ../hw3_backend/comment_map/map.html")
    end
end