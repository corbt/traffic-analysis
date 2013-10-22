require 'rubygems'
require 'json'
require 'jsonpath'
require './utils/rarff'

jsonfile=ARGV[0]
pathsfile=ARGV[1]
relationName = ARGV[2]
outfile=ARGV[3]

def convertPathToAttributeName(path)
  return path.gsub(/[\[\]$\/.]/, '_').gsub(/[*]/,'ANY')
end
paths = File.readlines(pathsfile)
attributes = []
meta = []
paths.each do |pathspec|
  (path, type) = pathspec.split(/\t/)
  name = convertPathToAttributeName(path)
  attribute = Rarff::Attribute.new(name=name,type=type)
  attribute.check_nominal
  meta.push({"name" => name,
              "path" => path,
              "pathConverter" => JsonPath.new(path),
              "type" => type})
  attributes.push(attribute)
end

relation = Rarff::Relation.new(relationName)
instances = []
JSON.parse(IO.read("C:/Users/djhaskin814/Workspace/IntelliJ/traffic-analysis/data/latest.json")).each do |record|
  instance = []
  meta.each do |datums|
    data = datums['pathConverter'].first(record)
    if datums['type'] == "STRING"
      data = data.gsub(/['"]/,"-")
    end
    instance.push(data)
  end
  instances.push(instance)
end
relation.instances = instances
relation.attributes = attributes
File.open(outfile, "w") do |out|
  out.puts relation.to_arff
end
