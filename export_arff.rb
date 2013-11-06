require 'rubygems'
require 'json'
require './utils/rarff'
require 'csv'
require 'json'

jsonfile=ARGV[0]
pathsfile=ARGV[1]
relationName = ARGV[2]
outfile=ARGV[3]

def convertPathToAttributeName(path)
  return path.gsub(/[\[\]$\/.]/, '_').gsub(/[*]/,'ANY')
end

attributes = []

pathObjs = []
CSV.foreach(pathsfile, :headers => true) do |row|
  pathObjs.push({
    "name" => row["name"],
    "path" => row["path"],
    "type" => row["type"]
    })
  attribute = Rarff::Attribute.new(name=row["name"], type=row["type"])
  attribute.check_nominal
  attributes.push(attribute)
end

relation = Rarff::Relation.new(relationName)
instances = []

i = 0
JSON.parse(IO.read(jsonfile)).each do |incident|
  instance = []
  pathObjs.each do |pathObj|   
    json = incident
    splitpath = pathObj["path"].split('/')
    splitpath.each do |nextJSONattr|
      if nextJSONattr != ""        
        bracketIndex = nextJSONattr.rindex('[')
        if bracketIndex == nil
          key = nextJSONattr
        else
          key = nextJSONattr[0..bracketIndex-1]
          index_in_array = nextJSONattr[bracketIndex+1..nextJSONattr.length-2]
        end
        if json[key] == nil
          puts "couldn't find attribute '"+key+"' in path '"+pathObj["path"]+"'"
          puts "json = "+json.inspect
        end
        json = json[key]
        if index_in_array != nil
          json = json[index_in_array.to_i]
        end
      end
    end
    
    if pathObj["type"] == "LENGTH"
      json = json.length
    end
    instance.push(json)
    # instance.push("\""+json+"\"")


    # data = datums['path'].first(record)
    # if datums['type'] == "STRING"
    #   data = data.gsub(/['"]/,"-")
    # end
    # instance.push(data)
  end
  instances.push(instance)
end
relation.instances = instances
relation.attributes = attributes
File.open(outfile, "w") do |out|
  out.puts relation.to_arff
end
