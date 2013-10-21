require 'net/http'

Region = Struct.new :coord1, :coord2, :name

regions = [
	Region.new("50.26,-2.77","53.6,1.9","london"),
	Region.new("56.52,18.7","60,20.3","stockholm"),
	# Region.new("40.52,-0.239","42.146,3.5","barcelona"),
	Region.new("39.95,-112.37","40.93,-111.48","slc"),
	Region.new("47.15,-122.58","48.013,-121.843","seattle"),
	Region.new("37.0,-122.8","38,-121.64","sf"),
	Region.new("33.8,-118.36","34.2,-117.6","la"),
	Region.new("40.59,-74.2","41.1,-73.39","nyc"),
	Region.new("52.33,13.5","52.71,13.71","berlin"),
	Region.new("48.55,1.97","49.1,2.76","paris"),
	# Region.new("-33.94,-71.31","-33.04,-69.89","santiago"),
	# Region.new("35.22,140.41","36.41,140.74","tokyo"),
]

namespace :cs478 do 
	desc "Poll the Bing incidents API"
	task :slurp_bing => :environment do
		puts Time.now
		regions.each do |region|
			puts "\tProcessing region #{region.name}"

			url = URI.parse("http://dev.virtualearth.net/REST/v1/Traffic/Incidents/#{region.coord1},#{region.coord2}?t=1&key=#{ML478::BING_KEY}")
			req = Net::HTTP::Get.new(url.to_s)
			data = Net::HTTP.start(url.host, url.port) {|http| http.request(req) }
			json = JSON.parse(data.body)
			json['resourceSets'][0]['resources'].each do |incident|
				id = incident['incidentId']
				if Incident.find_by_incidentId(id).nil?
					puts "\t\tpersisting incident #{id}"
					weather = get_weather incident
					traffic = get_traffic incident
					Incident.create(blob: JSON.pretty_generate(incident), incidentId: id, region: region.name, weather: weather, traffic: traffic)					
				else
					puts "\t\tduplicate incident #{id} discarded"
				end
			end
		end
	end
end

def get_weather incident
	begin
		coords = incident['point']['coordinates']
		sleep 7.seconds # because of API throttling
		url = URI.parse("http://api.wunderground.com/api/#{ML478::WU_KEY}/conditions/astronomy/q/#{coords[0]},#{coords[1]}.json")
		req = Net::HTTP::Get.new(url.to_s)
		data = Net::HTTP.start(url.host, url.port) {|http| http.request(req) }
		puts "\t\t\tweather lookup successful"
		data.body
	rescue
		puts "\t\t\tweather lookup failed"
	end
end

def get_traffic incident
	begin
		coords = incident['point']['coordinates']
		sleep 7.seconds # because of API throttling
		url = URI.parse("http://dev.virtualearth.net/REST/v1/Routes/FromMajorRoads?dest=#{coords[0]},#{coords[1]}&du=Mile&key=#{ML478::BING_KEY}")
		req = Net::HTTP::Get.new(url.to_s)
		data = Net::HTTP.start(url.host, url.port) {|http| http.request(req) }
		puts "\t\t\ttraffic lookup successful"
	rescue
		puts "\t\t\ttraffic lookup failed"
	end