require 'rubygems'
require 'json'
require 'jsonpath'
require './utils/rarff'
require 'optparse'

options = OpenStruct.new
options.relationName = "TrafficData"
parser = OptionParser.new do |opts|
  opts.banner = "Usage: export_arff.rb [options] <jsonfile> <pathsfile> <outfile>"
  opts.separator ""
  opts.separator "  Where:"
  opts.on("-r","--relation-name [NAME]", String, "Specify relation name") do |r|
    options.relationName = r
  end
  opts.on_tail("-h", "--help", "display this help page") do |h|
    puts opts
    exit
  end
end
parser.parse!(ARGV)
if  ARGV.length != 3
  puts "Wrong number of arguments."
  puts "Use '-h' option for more details."
  exit
end
jsonfile=ARGV[0]
pathsfile=ARGV[1]
outfile=ARGV[2]
relationName=options.relationName

def convertPathToAttributeName(path)
  return path.gsub(/[\[\]$\/._-]/, '')
    .gsub(/[*]/,'ANY')
    .gsub(/[0]/,'Zero')
    .gsub(/[1]/,'One')
    .gsub(/[2]/,'Two')
    .gsub(/[3]/,'Three')
    .gsub(/[4]/,'Four')
    .gsub(/[5]/,'Five')
    .gsub(/[6]/,'Six')
    .gsub(/[7]/,'Seven')
    .gsub(/[8]/,'Eight')
    .gsub(/[9]/,'Nine')
end
lines = File.readlines(pathsfile)
attributes = []
meta = []
lines.each do |pathspec|
  pathspec.strip!
  if /^$/ =~ pathspec
      next
  end
  path = pathspec.sub(/^([^[:space:]]*)[[:space:]].*$/,'\1')
  type = pathspec.sub(/^[^[:space:]]*[[:space:]]+/,'')
  name = convertPathToAttributeName(path)
  attribute = Rarff::Attribute.new(name=name,type=type)
  attribute.check_nominal
  puts "Attempting to add path '#{path}'..."
  puts "Path = #{path}"
  puts "Type = #{type}"
  meta.push({"name" => name,
              "path" => path,
              "pathConverter" => JsonPath.new(path),
              "type" => type})
  attributes.push(attribute)
end

relation = Rarff::Relation.new(relationName)
instances = []
JSON.parse(IO.read(jsonfile)).each do |record|
  instance = []
  meta.each do |datums|
    data = datums['pathConverter'].first(record)
    if datums['type'] == "STRING"
      data = data.gsub(/['"]/,"-")
    end
    if data.class == String
      data = data.gsub(/N\/A/,"?")
    elsif data == nil
      data = "?"
    elsif data.class == Float
      if (data).round == -999
        data = "?"
      end
    end
    instance.push(data)
  end
  instances.push(instance)
end
relation.instances = instances
relation.attributes = attributes
File.open(outfile, "w") do |out|
  # Get rid of missing values
  arff = relation.to_arff
  lines = arff.split(/\r?\n/)
  lines.each do |line|
    if not (/, *,/ =~ line)
      out.puts line
    end
  end
end
