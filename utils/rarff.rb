# = rarff

# Copyright (c) 2006-2012 Andy Payne
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 	* Redistributions of source code must retain the above copyright notice,
#         this list of conditions and the following disclaimer.
# 	* Redistributions in binary form must reproduce the above copyright notice,
#         this list of conditions and the following disclaimer in the
#         documentation and/or other materials provided with the distribution.
# 	* Neither the name of the COPYRIGHT OWNER nor the names of its contributors
#         may be used to endorse or promote products derived from this software
#         without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# This is the top-level include file for rarff. See the README file for
# details.

################################################################################

# Custom scan that returns a boolean indicating whether the regex matched.
# TODO: Is there a way to avoid doing this?
class String
  def my_scan(re)
    hit = false
    scan(re) { |arr|
      yield arr if block_given?
      hit = true
    }
    hit
  end
end

################################################################################

module Enumerable
# This map_with_index hack allows access to the index of each item as the map
# iterates.
# TODO: Is there a better way?
  def map_with_index
    # Ugly, but I need the yield to be the last statement in the map.
    i = -1
    return map { |item|
      i += 1
      yield item, i
    }
  end
end

################################################################################

module Rarff

  COMMENT_MARKER = '%'
  RELATION_MARKER = '@RELATION'
  ATTRIBUTE_MARKER = '@ATTRIBUTE'
  DATA_MARKER = '@DATA'

  SPARSE_ARFF_BEGIN = '{'
  ESC_SPARSE_ARFF_BEGIN = '\\' + SPARSE_ARFF_BEGIN
  SPARSE_ARFF_END = '}'
  ESC_SPARSE_ARFF_END = '\\' + SPARSE_ARFF_END

  ATTRIBUTE_NUMERIC = 'NUMERIC'
  ATTRIBUTE_REAL = 'REAL'
  ATTRIBUTE_INTEGER = 'INTEGER'
  ATTRIBUTE_STRING = 'STRING'
  ATTRIBUTE_DATE = 'DATE'


################################################################################

  class Attribute
    attr_accessor :name, :type

    def initialize(name='', type='')
      @name = name

      @type_is_nominal = false
      @type = type

      check_nominal()
    end


    def type=(type)
      @type = type
      check_nominal()
    end


    # Convert string representation of nominal type to array, if necessary
    # TODO: This might falsely trigger on wacky date formats.
    def check_nominal
      if @type =~ /^\s*\{.*(\,.*)+\}\s*$/
        @type_is_nominal = true
        # Example format: "{nom1,nom2, nom3, nom4,nom5 } "
        # Split on '{'  ','  or  '}'
        @type = @type.gsub(/^\s*\{\s*/, '').gsub(/\s*\}\s*$/, '').split(/\s*\,\s*/)
      end
    end


    def add_nominal_value(str)
      if @type_is_nominal == false
        @type = Array.new
      end

      @type << str
    end


    def to_arff
      if @type_is_nominal == true
        ATTRIBUTE_MARKER + " #{@name} " + '{ ' + "#{@type.join(',')}" + ' }'
      else
        ATTRIBUTE_MARKER + " #{@name} #{@type}"
      end
    end


    def to_s
      to_arff
    end

  end

  Comment = Struct.new(:text,:row)

  class Relation
    attr_accessor :name, :attributes, :instances, :comments


    def initialize(name='')
      @name = name
      @attributes = Array.new
      @instances = Array.new
      @comments = Array.new
    end


    def parse(str)
      in_data_section = false

      # TODO: Doesn't handle commas in quoted attributes.
      str.split("\n").each_with_index { |line, idx|
        next if line =~ /^\s*$/
        next if line.my_scan(/^\s*#{COMMENT_MARKER}/) { @comments << Comment.new(line.slice(1..-1), idx+1)}
        next if line.my_scan(/^\s*#{RELATION_MARKER}\s*(.*)\s*$/i) { |name| @name = name }
        next if line.my_scan(/^\s*#{ATTRIBUTE_MARKER}\s*([^\s]*)\s+(.*)\s*$/i) { |name, type|
          @attributes.push(Attribute.new(name, type))
        }
        next if line.my_scan(/^\s*#{DATA_MARKER}/i) { in_data_section = true }
        next if in_data_section == false ## Below is data section handling
                                         #			next if line.gsub(/^\s*(.*)\s*$/, "\\1").my_scan(/^\s*#{SPARSE_ARFF_BEGIN}(.*)#{SPARSE_ARFF_END}\s*$/) { |data|
        next if line.gsub(/^\s*(.*)\s*$/, "\\1").my_scan(/^#{ESC_SPARSE_ARFF_BEGIN}(.*)#{ESC_SPARSE_ARFF_END}$/) { |data|
          # Sparse ARFF
          # TODO: Factor duplication with non-sparse data below
          @instances << expand_sparse(data.first)
          create_attributes()
        }
        next if line.my_scan(/^\s*(.*)\s*$/) { |data|
          @instances << data.first.split(/,\s*/).map { |field|
            # Remove outer single quotes on strings, if any ('foo bar' --> foo bar)
            field.gsub(/^\s*\'(.*)\'\s*$/, "\\1")
          }
          create_attributes()
        }
      }
    end


    def instances=(instances)
      @instances = instances
      create_attributes()
    end


    def create_attributes
      attr_pass = true

      @instances.each_index { |i|
        @instances[i].each_index { |j|
          if @instances[i][j].class != String
            assign_or_build_attr(j, ATTRIBUTE_NUMERIC) if attr_pass
          elsif @instances[i][j] =~ /^\-?\d+\.?\d*$/
            # TODO: Should I have a separate to_i conversion, or is to_f sufficient?
            @instances[i][j] = @instances[i][j].to_f
            assign_or_build_attr(j, ATTRIBUTE_NUMERIC) if attr_pass
          else
            assign_or_build_attr(j, ATTRIBUTE_STRING) if attr_pass
          end
        }

        attr_pass = false
      }
    end


    def assign_or_build_attr(j, attr_type)
      if @attributes[j].is_a?(Attribute)
        @attributes[j].type = attr_type
      else
        @attributes[j] = Attribute.new("Attr#{j}", attr_type)
      end
    end

    def expand_sparse(str)
      arr = Array.new(@attributes.size, 0)
      str.gsub(/^\s*\{(.*)\}\s*$/, "\\1").split(/\s*\,\s*/).map { |pr|
        pra = pr.split(/\s/)
        arr[pra[0].to_i] = pra[1]
      }
      arr
    end


    def to_arff
      RELATION_MARKER + " #{@name}\n" +
          @attributes.map { |attr| attr.to_arff }.join("\n") +
          "\n" +
          DATA_MARKER + "\n" +
          @instances.map { |inst|
            inst.map_with_index { |col, i|
              # Quote strings with spaces.
              # TODO: Doesn't handle cases in which strings already contain
              # quotes or are already quoted.
              if @attributes[i].type =~ /^#{ATTRIBUTE_STRING}$/i
                if col =~ /\s+/
                  col = "'" + col.gsub(/['"]/,"`") + "'"
                end
              elsif @attributes[i].type =~ /^#{ATTRIBUTE_DATE}/i ## Hack comparison. Ugh.
                col = '"' + col + '"'
              end
              col
            }.join(', ')
          }.join("\n")
    end


    def to_s
      to_arff
    end

  end


end # module Rarff

################################################################################

if $0 == __FILE__

  exit unless ARGV[0]
  in_file = ARGV[0]
  contents = ''

  contents = File.open(in_file).read

  rel = Rarff::Relation.new
  rel.parse(contents)

  puts '='*80
  puts '='*80
  puts "ARFF:"
  puts rel

end

################################################################################


